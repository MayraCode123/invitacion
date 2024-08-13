import cv2
import numpy as np
from pyzbar.pyzbar import decode

def process_frame(frame):
    # Convertir el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar y decodificar códigos QR
    decoded_objects = decode(gray)
    
    for obj in decoded_objects:
        # Dibujar el rectángulo alrededor del código QR
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((4, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        else:
            hull = cv2.convexHull(np.array(points, dtype=np.float32))
            cv2.polylines(frame, [np.array(hull, dtype=np.int32)], True, (0, 255, 0), 2)
        
        # Decodificar el texto del QR
        qr_data = obj.data.decode('utf-8')
        qr_type = obj.type
        text = f"{qr_data} ({qr_type})"
        
        # Mostrar el texto del QR
        cv2.putText(frame, text, (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame

def main():
    # Abrir la cámara
    cap = cv2.VideoCapture(0)
    
    while True:
        # Capturar el frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Procesar el frame para leer QR
        frame = process_frame(frame)
        
        # Mostrar el frame en la ventana
        cv2.imshow('QR Code Reader', frame)
        
        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar la cámara y cerrar las ventanas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
