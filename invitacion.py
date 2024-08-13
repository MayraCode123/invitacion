import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image

data = "https://docs.google.com/forms/d/e/1FAIpQLScV4dOzVz7ipBmcuuXoupl-ki54n9W4wrZRmSnXQVn7wS0vRA/viewform?usp=sf_link"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Mayor nivel de corrección de errores para logotipos
    box_size=10,
    border=4,
)

qr.add_data(data)
qr.make(fit=True)

# Crear la imagen del QR con un estilo personalizado
img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(), 
    color_mask=RadialGradiantColorMask(back_color=(255, 255, 255), center_color=(0, 0, 0), edge_color=(0, 0, 255)),
)

# Convertir la imagen del QR a un formato RGBA (con transparencia)
img = img.convert("RGBA")

# Cargar el logotipo que deseas poner en el centro del QR
logo = Image.open("logo.png")

# Calcular el tamaño adecuado para el logotipo (por ejemplo, 25% del tamaño del QR)
logo_size = (img.size[0] // 4, img.size[1] // 4)
logo = logo.resize(logo_size, Image.LANCZOS)  # Usar Image.LANCZOS en lugar de Image.ANTIALIAS

# Calcular la posición donde el logotipo debe ser colocado
pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)

# Crear un fondo blanco en la zona donde se colocará el logotipo
background = Image.new("RGBA", img.size, (255, 255, 255, 0))  # Fondo transparente
white_box = Image.new("RGBA", logo.size, (255, 255, 255, 255))  # Cuadro blanco del tamaño del logotipo
background.paste(white_box, pos)

# Combinar el fondo blanco con el código QR
img = Image.alpha_composite(img, background)

# Superponer el logotipo en el QR
img.paste(logo, pos, mask=logo)

# Guardar la imagen final con el logotipo en el centro
img.save("codigo_qr_con_logo.png")

print("Código QR generado y guardado como 'codigo_qr_con_logo.png'")
