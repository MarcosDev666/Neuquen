"""
scene.py — Motor mínimo de escenas 2D con dos backends: SVG (vector) y PNG (Pillow).

Las escenas trabajan en metros locales (x=este, y=norte) y se "ajustan" a la
caja visible con un factor de escala único (sin distorsión vertical/horizontal).
"""
import math
import os

# ------------------------------------------------------------------ op constructors
def polygon(pts, fill, stroke=None, width=0.0, opacity=1.0, dash=None):
    return {"op": "polygon", "pts": pts, "fill": fill, "stroke": stroke,
            "width": width, "opacity": opacity, "dash": dash}

def polyline(pts, stroke, width, opacity=1.0, dash=None, cap="round", join="round"):
    return {"op": "polyline", "pts": pts, "stroke": stroke, "width": width,
            "opacity": opacity, "dash": dash, "cap": cap, "join": join}

def circle(c, r, fill, stroke=None, width=0.0, opacity=1.0):
    return {"op": "circle", "c": c, "r": r, "fill": fill, "stroke": stroke,
            "width": width, "opacity": opacity}

def text(pos, s, size, fill, anchor="middle", weight="normal", opacity=1.0,
         spacing=0.0, rotate=0.0, halo=True, halo_color="#f5f1e6"):
    return {"op": "text", "pos": pos, "s": s, "size": size, "fill": fill,
            "anchor": anchor, "weight": weight, "opacity": opacity,
            "spacing": spacing, "rotate": rotate, "halo": halo,
            "halo_color": halo_color}

def rect(x, y, w, h, fill, stroke=None, width=0.0, opacity=1.0):
    return {"op": "rect", "x": x, "y": y, "w": w, "h": h, "fill": fill,
            "stroke": stroke, "width": width, "opacity": opacity}

class Scene:
    def __init__(self, title, world_bbox, margin_px=8):
        """world_bbox = (x0, y0, x1, y1) en metros locales."""
        self.title = title
        self.ops = []
        self.x0, self.y0, self.x1, self.y1 = world_bbox
        self.margin = margin_px

    def add(self, op):
        self.ops.append(op)

    # ------------------------------------------------------------------ fitting
    def view(self, width_px, height_px):
        wx, wy = (self.x1 - self.x0), (self.y1 - self.y0)
        s = min((width_px - 2 * self.margin) / wx, (height_px - 2 * self.margin) / wy)
        ox = (width_px - wx * s) / 2.0
        oy = (height_px - wy * s) / 2.0
        return s, ox, oy

    def to_px(self, x, y, s, ox, oy, height_px):
        return ox + (x - self.x0) * s, height_px - (oy + (y - self.y0) * s)

    # ------------------------------------------------------------------ svg
    def render_svg(self, path, width_px=2400, height_px=1700):
        s, ox, oy = self.view(width_px, height_px)

        def P(pt):
            x, y = self.to_px(pt[0], pt[1], s, ox, oy, height_px)
            return f"{x:.2f},{y:.2f}"

        def pts(pts_):
            if len(pts_) == 1:
                return P(pts_[0])
            return " ".join(P(p) for p in pts_)

        def col(c, opacity=1.0):
            return c if opacity >= 1.0 else c

        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_px}" height="{height_px}" '
               f'viewBox="0 0 {width_px} {height_px}" role="img" aria-label="{self.title}">']
        out.append(f"<title>{self.title}</title>")
        svg_dash = {None: None, "rail": "14 7", "short": "7 6", "long": "26 12", "dot": "2 6"}
        for op in self.ops:
            t = op["op"]
            if t == "rect":
                x, y = self.to_px(op["x"], op["y"] + op["h"], s, ox, oy, height_px)
                w, h = op["w"] * s, op["h"] * s
                opact = f' fill-opacity="{op["opacity"]}"' if op["opacity"] < 1 else ""
                stroke = f' stroke="{op["stroke"]}" stroke-width="{op["width"]*s:.2f}"' if op.get("stroke") else ""
                out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{op["fill"]}"{opact}{stroke}/>')
            elif t == "polygon":
                extra = []
                if op.get("stroke"):
                    extra.append(f'stroke="{op["stroke"]}"'); extra.append(f'stroke-width="{op["width"]*s:.2f}"')
                    extra.append('stroke-linejoin="round"')
                if op.get("dash"):
                    extra.append(f'stroke-dasharray="{svg_dash.get(op["dash"], op["dash"])}"')
                fill = f'fill="{op["fill"]}"' if op["fill"] else 'fill="none"'
                opact = f' opacity="{op["opacity"]}"' if op["opacity"] < 1 else ""
                tail = (" " + " ".join(extra)) if extra else ""
                out.append(f'<polygon points="{pts(op["pts"])}" {fill}{tail}{opact}/>')
            elif t == "polyline":
                dash = f' stroke-dasharray="{svg_dash.get(op.get("dash"), op["dash"])}"' if op.get("dash") else ""
                opact = f' opacity="{op["opacity"]}"' if op["opacity"] < 1 else ""
                out.append(f'<polyline points="{pts(op["pts"])}" fill="none" stroke="{op["stroke"]}" '
                           f'stroke-width="{op["width"]*s:.2f}" stroke-linecap="{op["cap"]}" '
                           f'stroke-linejoin="{op["join"]}"{dash}{opact}/>')
            elif t == "circle":
                cx, cy = self.to_px(op["c"][0], op["c"][1], s, ox, oy, height_px)
                r = op["r"] * s
                stroke = f' stroke="{op["stroke"]}" stroke-width="{op["width"]*s:.2f}"' if op.get("stroke") else ""
                opact = f' opacity="{op["opacity"]}"' if op["opacity"] < 1 else ""
                out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{op["fill"]}"{stroke}{opact}/>')
            elif t == "text":
                cx, cy = self.to_px(op["pos"][0], op["pos"][1], s, ox, oy, height_px)
                anchor = {"start": "start", "middle": "middle", "end": "end"}[op["anchor"]]
                weight = "700" if op["weight"] == "bold" else "400"
                style = f'paint-order:stroke;stroke:{op["halo_color"]};stroke-width:{max(2.0, op["size"]/4.2):.1f}px;stroke-linejoin:round'
                spacing = f' letter-spacing="{op["spacing"]}"' if op["spacing"] else ""
                rotate = f' transform="rotate({-op["rotate"]} {cx:.2f} {cy:.2f})"' if op["rotate"] else ""
                opact = f' opacity="{op["opacity"]}"' if op["opacity"] < 1 else ""
                lines = op["s"].split("\n")
                line_h = op["size"] * 1.18
                first_baseline = cy - (len(lines) - 1) * line_h / 2 + op["size"] * 0.35
                tspans = []
                for i, ln in enumerate(lines):
                    esc = ln.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    dy = "0" if i == 0 else f"{line_h:.2f}"
                    tspans.append(f'<tspan x="{cx:.2f}" dy="{dy}">{esc}</tspan>')
                out.append(f'<text x="{cx:.2f}" y="{first_baseline:.2f}" font-family="DejaVu Sans, Arial, sans-serif" '
                           f'font-size="{op["size"]}" font-weight="{weight}" fill="{op["fill"]}" '
                           f'text-anchor="{anchor}" style="{style}"{spacing}{rotate}{opact}>' + "".join(tspans) + "</text>")
        out.append("</svg>")
        xml = "\n".join(out)
        with open(path, "w") as f:
            f.write(xml)
        return path

    # ------------------------------------------------------------------ png
    def render_png(self, path, width_px=2400, height_px=1700):
        from PIL import Image, ImageDraw, ImageFont
        s, ox, oy = self.view(width_px, height_px)
        img = Image.new("RGB", (width_px, height_px), "#f5f1e6")
        d = ImageDraw.Draw(img, "RGBA")
        FD = "/usr/share/fonts/truetype/dejavu/"

        def font(size, weight="normal"):
            name = "DejaVuSans-Bold.ttf" if weight == "bold" else "DejaVuSans.ttf"
            return ImageFont.truetype(FD + name, int(size))

        def PT(pt):
            return self.to_px(pt[0], pt[1], s, ox, oy, height_px)

        def hexrgba(c, op=1.0):
            c = c.lstrip("#")
            if len(c) == 3:
                c = "".join(ch * 2 for ch in c)
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            return (r, g, b, int(255 * op))

        dash_pat = {"rail": (14, 7), "short": (7, 6), "long": (26, 12), "dot": (2, 6)}

        def dashed(points, dash_key):
            pat = dash_pat.get(dash_key, (10, 6)) if isinstance(dash_key, str) else dash_key
            on_len, off_len = pat
            result = []
            cur = []
            state_on = True
            remaining_in_piece = on_len
            for a, b in zip(points, points[1:]):
                ax, ay = a; bx, by = b
                seglen = math.dist(a, b)
                if seglen == 0:
                    continue
                ux, uy = (bx - ax) / seglen, (by - ay) / seglen
                pos = 0.0
                posx, posy = ax, ay
                while pos < seglen:
                    step = min(remaining_in_piece, seglen - pos)
                    nx, ny = posx + ux * step, posy + uy * step
                    if state_on:
                        if not cur:
                            cur = [(posx, posy)]
                        cur.append((nx, ny))
                    else:
                        if len(cur) >= 2:
                            result.append(cur)
                        cur = []
                    posx, posy = nx, ny
                    pos += step
                    remaining_in_piece -= step
                    if remaining_in_piece <= 1e-9:
                        state_on = not state_on
                        remaining_in_piece = on_len if state_on else off_len
            if cur and len(cur) >= 2:
                result.append(cur)
            return result

        for op in self.ops:
            t = op["op"]
            if t == "rect":
                x, y = PT((op["x"], op["y"] + op["h"]))
                w, h = op["w"] * s, op["h"] * s
                d.rectangle([x, y, x + w, y + h], fill=hexrgba(op["fill"], op["opacity"]))
            elif t == "polygon":
                pts = [PT(p) for p in op["pts"]]
                if op["fill"]:
                    d.polygon(pts, fill=hexrgba(op["fill"], op["opacity"]))
                if op.get("stroke"):
                    d.line(pts + [pts[0]], fill=hexrgba(op["stroke"], op["opacity"]),
                           width=max(1, round(op["width"] * s)), joint="curve")
            elif t == "polyline":
                pts = [PT(p) for p in op["pts"]]
                wpx = max(1, round(op["width"] * s))
                col = hexrgba(op["stroke"], op["opacity"])
                if op.get("dash"):
                    for seg in dashed(pts, op["dash"]):
                        d.line(seg, fill=col, width=wpx, joint="curve")
                else:
                    d.line(pts, fill=col, width=wpx, joint="curve")
            elif t == "circle":
                cx, cy = PT(op["c"])
                r = op["r"] * s
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexrgba(op["fill"], op["opacity"]))
                if op.get("stroke"):
                    d.ellipse([cx - r, cy - r, cx + r, cy + r],
                              outline=hexrgba(op["stroke"], op["opacity"]),
                              width=max(1, round(op["width"] * s)))
            elif t == "text":
                cx, cy = PT(op["pos"])
                fnt = font(op["size"], op["weight"])
                lines = op["s"].split("\n")
                asc, desc = fnt.getmetrics()
                line_h = (asc + desc) * 1.18
                hw = max(2, round(op["size"] / 5)) if op["halo"] else 0

                def measure(ln):
                    if op["spacing"]:
                        ws = [d.textlength(ch, font=fnt) for ch in ln]
                        return sum(ws) + op["spacing"] * max(0, len(ln) - 1), ws
                    return d.textlength(ln, font=fnt), None

                measured = [measure(ln) for ln in lines]
                total_w = max((w for w, _ in measured), default=0)
                total_h = line_h * len(lines)
                pad = 4
                tile_w = int(total_w + 2 * hw + 2 * pad + 1)
                tile_h = int(total_h + 2 * hw + 2 * pad + 1)
                tile = Image.new("RGBA", (max(1, tile_w), max(1, tile_h)), (0, 0, 0, 0))
                td = ImageDraw.Draw(tile)
                for i, ln in enumerate(lines):
                    lw, ws = measured[i]
                    if op["anchor"] == "middle":
                        sx = (tile_w - lw) / 2
                    elif op["anchor"] == "end":
                        sx = tile_w - lw - hw - pad
                    else:
                        sx = hw + pad
                    sy = hw + pad + i * line_h
                    if op["halo"]:
                        halo_c = hexrgba(op["halo_color"], 0.9)
                        for dx in (-hw, 0, hw):
                            for dy in (-hw, 0, hw):
                                if dx or dy:
                                    _draw_text_spaced(td, sx + dx, sy + dy, ln, fnt, ws,
                                                      op["spacing"], halo_c)
                    _draw_text_spaced(td, sx, sy, ln, fnt, ws,
                                      op["spacing"], hexrgba(op["fill"], op["opacity"]))
                if op["rotate"]:
                    tile = tile.rotate(op["rotate"], resample=Image.BICUBIC, expand=True)
                    img.paste(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)), tile)
                else:
                    if op["anchor"] == "start":
                        px = int(cx - hw - pad)
                    elif op["anchor"] == "end":
                        px = int(cx - tile_w + hw + pad)
                    else:
                        px = int(cx - tile_w / 2)
                    img.paste(tile, (px, int(cy - tile_h / 2)), tile)
        img.save(path)
        return path

def _draw_text_spaced(td, x, y, txt, fnt, widths, spacing, fill):
    if not widths:
        td.text((x, y), txt, font=fnt, fill=fill)
        return
    px = x
    for ch, w in zip(txt, widths):
        td.text((px, y), ch, font=fnt, fill=fill)
        px += w + spacing
