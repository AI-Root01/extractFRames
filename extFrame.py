import cv2
import os

# Función para mejorar la calidad de la imagen a color
def improve_image_quality(image):
    # Aplicar un filtro bilateral para suavizar sin perder bordes (manteniendo el color)
    image_bilateral = cv2.bilateralFilter(image, 9, 75, 75)

    # Convertir la imagen a LAB para mejorar el contraste
    lab_image = cv2.cvtColor(image_bilateral, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)

    # Mejorar el canal L (luminosidad) usando CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)

    # Combinar de nuevo los canales
    lab_image_clahe = cv2.merge((l_clahe, a, b))
    
    # Convertir de vuelta a BGR (color)
    return cv2.cvtColor(lab_image_clahe, cv2.COLOR_LAB2BGR)

# Ruta de la carpeta con los videos
video_folder = 'VideosParaFrame'

# Recorrer todos los videos en la carpeta
for video_file in os.listdir(video_folder):
    video_path = os.path.join(video_folder, video_file)

    if video_file.endswith('.mp4') or video_file.endswith('.avi'):  # Puedes agregar otros formatos si es necesario
        # Crear una carpeta para cada video dentro de la carpeta de los videos
        video_name = os.path.splitext(video_file)[0]
        video_output_dir = os.path.join(video_folder, video_name)  # Crear carpeta dentro de la carpeta de videos
        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)

        # Leer el video
        cap = cv2.VideoCapture(video_path)
        frame_number = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break  # Salir si no hay más frames

            # Mejorar la calidad del frame a color
            improved_frame = improve_image_quality(frame)

            # Guardar el frame en la carpeta correspondiente
            frame_filename = os.path.join(video_output_dir, f"frame_{frame_number:04d}.png")
            cv2.imwrite(frame_filename, improved_frame)  # Guardar como PNG para no perder calidad
            frame_number += 1

        cap.release()

print("Extracción de frames completada.")

