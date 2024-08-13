import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image, ImageDraw, ImageFont

# URL base del formulario
form_url_base = "https://docs.google.com/forms/d/e/1FAIpQLScV4dOzVz7ipBmcuuXoupl-ki54n9W4wrZRmSnXQVn7wS0vRA/viewform?usp=sf_link"

# Lista de personas con identificadores únicos
personas = [
    {"nombre": "Juan Pérez", "id": 1},
    {"nombre": "María López", "id": 2},
    {"nombre": "Carlos Ramírez", "id": 3},
    {"nombre": "Andreina Caballero", "id": 4},
]

# Fuente para el texto (asegúrate de que la fuente exista en tu sistema o usa una incluida)
font_path = "ariali.ttf"
font_size = 20  # Tamaño del texto

# Ruta del logo
logo_path = "logo.png"  # Cambia la ruta a la ubicación de tu logo

# Tamaño del logo en relación con el QR
logo_size_ratio = 0.2  # El tamaño del logo será el 20% del QR

for persona in personas:
    # Personalizar la URL para cada persona
    data = f"{form_url_base}&id={persona['id']}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(back_color=(255, 255, 255), center_color=(0, 0, 0), edge_color=(0, 0, 0)),
    )

    img = img.convert("RGBA")

    # Cargar y redimensionar el logo
    logo = Image.open(logo_path).convert("RGBA")
    logo_size = int(min(img.size) * logo_size_ratio)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Crear una imagen de fondo blanco para el logo
    background = Image.new("RGBA", (logo_size, logo_size), (255, 255, 255, 255))
    background.paste(logo, (0, 0), logo)  # Pega el logo en el fondo blanco

    # Calcular la posición para centrar el logo
    logo_position = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)

    # Añadir el logo al código QR
    img.paste(background, logo_position, background)

    # Crear una nueva imagen para añadir el texto debajo del QR
    font = ImageFont.truetype(font_path, font_size)
    
    # Obtener las dimensiones del texto
    text_bbox = font.getbbox(persona["nombre"])
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Calcular el tamaño de la nueva imagen (QR + espacio para el texto)
    new_img_height = img.size[1] + text_height + 10  # 10 píxeles de margen
    new_img = Image.new("RGBA", (img.size[0], new_img_height), (255, 255, 255, 255))

    # Pegar el QR con el logo en la nueva imagen
    new_img.paste(img, (0, 0))

    # Dibujar el texto debajo del QR
    draw = ImageDraw.Draw(new_img)
    text_position = ((new_img.size[0] - text_width) // 2, img.size[1] + 5)  # Centrado horizontalmente y con margen
    draw.text(text_position, persona["nombre"], font=font, fill=(0, 0, 0))

    # Guardar la imagen final con el QR, el logo y el nombre
    nombre_archivo = f"codigo_qr_{persona['nombre'].replace(' ', '_').lower()}.png"
    new_img.save(nombre_archivo)

    print(f"Código QR generado para {persona['nombre']} y guardado como '{nombre_archivo}'")