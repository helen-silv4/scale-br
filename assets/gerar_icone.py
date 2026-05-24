"""
Gera o arquivo de ícone (.ico) do SCALE-BR a partir do tema da splash:
fundo azul arredondado + emoji 🌱 centralizado.
Execute uma vez quando quiser regenerar `scale_br.ico`.
"""

import os
from PIL import Image, ImageDraw, ImageFont

TAMANHO = 256
COR_FUNDO = "#1f6aa5"
COR_BORDA = "#145280"

img = Image.new("RGBA", (TAMANHO, TAMANHO), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

draw.rounded_rectangle(
    (4, 4, TAMANHO - 4, TAMANHO - 4),
    radius=44,
    fill=COR_FUNDO,
    outline=COR_BORDA,
    width=4,
)

# Tenta renderizar o emoji 🌱 colorido (Segoe UI Emoji no Windows).
# Em caso de falha, desenha um broto estilizado com primitivas.
emoji_desenhado = False
for fonte_path in (
    "C:/Windows/Fonts/seguiemj.ttf",
    "/System/Library/Fonts/Apple Color Emoji.ttc",
    "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
):
    if os.path.exists(fonte_path):
        try:
            fonte = ImageFont.truetype(fonte_path, 170)
            draw.text(
                (TAMANHO // 2, TAMANHO // 2 + 6),
                "🌱",
                font=fonte,
                anchor="mm",
                embedded_color=True,
            )
            emoji_desenhado = True
            break
        except Exception:
            continue

if not emoji_desenhado:
    cx, cy = TAMANHO // 2, TAMANHO // 2 + 20
    draw.rectangle((cx - 6, cy - 10, cx + 6, cy + 60), fill="white")
    draw.ellipse((cx - 70, cy - 60, cx - 5, cy + 5), fill="#7ed957")
    draw.ellipse((cx + 5, cy - 60, cx + 70, cy + 5), fill="#7ed957")

destino = os.path.join(os.path.dirname(__file__), "scale_br.ico")
img.save(
    destino,
    sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)
print(f"Ícone gerado em: {destino}")
