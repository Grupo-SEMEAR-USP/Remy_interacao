#No ROS 2 para visualizacao da imagem RGB da RealSense com leitura de profundidade
#
#Este programa recebe dois fluxos publicados pela RealSense:
#1. imagem RGB
#2. imagem de profundidade
#
#A imagem RGB e exibida normalmente com OpenCV
#A imagem decprofundidade e armazenada e usada para consultar a distancia do ponto central da imagem

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

from cv_bridge import CvBridge

import cv2

import numpy as np

#No responsavel por receber as imagens RGB e de profundidade publicadas pela RealSense
class CameraDepthNode(Node):
    
    def __init__(self):

        super().__init__('camera_depth_node')

        self.bridge = CvBridge()

        #variavel usada para armazenar a imagem de profundidade mais recente recebida.
        self.depth_frame = None

        #subscriber da imagem RGB
        self.rgb_subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.rgb_callback,
            10
        )

        #subscriber da imagem de profundidade
        self.depth_subscription = self.create_subscription(
            Image,
            '/camera/camera/aligned_depth_to_color/image_raw',
            self.depth_callback,
            10
        )

        self.get_logger().info(
            'Esperando imagens RGB e de profundidade da RealSense...'
        )


    #funcao chamada semre que uma nova imagem de profundidade e recebida 
    #a imagem e convertida do formato ROS para uma matriz que pode ser acessada pelo Python/OpenCV
    #cada posicao da matriz representa a profundidade medida naquele pixel
    def depth_callback(self, msg):
        
        #"passthrough" mantem o formato original dos dados de depth.
        self.depth_frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='passthrough'
        )

    #funcao chamada sempre que uma nova imagem RGB e recebida
    def rgb_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )

        #so tenta acessar a profundidade depois que pelo menos uma imagem depth ja tiver sido recebida
        if self.depth_frame is not None:

            #altura e largura da imagem RGB
            height, width = frame.shape[:2]

            #calcula as coordenadas do pixel central da imagem
            x = width // 2
            y = height // 2


    
            """
            #obtem o valor de profundidade naquele pixel
            depth_mm = self.depth_frame[y, x]

            #a realsense fornece a profundidade em milimetros
            #dividindo por 1000 obtemos metros
            depth_m = depth_mm / 1000.0
            """

            # Define uma pequena região ao redor do ponto central
            radius = 40

            cv2.rectangle(
                frame,
                (x - radius, y - radius),
                (x + radius, y + radius),
                (0, 255, 0),
                3
            )
                    

            depth_region = self.depth_frame[
                y - radius:y + radius + 1,
                x - radius:x + radius + 1
            ]

            # Remove valores inválidos de profundidade
            valid_depths = depth_region[depth_region > 0]

            if valid_depths.size > 0:
                # Usa a mediana da região para reduzir ruído
                depth_mm = np.median(valid_depths)
                depth_m = depth_mm / 1000.0
            else:
                depth_m = None

            #desenha um ponto vermelho indicando onde a profundidade esta sendo medida
            """cv2.circle(
                frame,
                (x, y),
                5,
                (0, 0, 255),
                -1
            )"""

            #escreve a distancia ao lado do ponto
            """cv2.putText(
                frame,
                f'{depth_m:.2f} m',
                (x + 10, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )"""

            if depth_m is not None:
                cv2.putText(
                    frame,
                    f'{depth_m:.2f} m',
                    (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )
            else:
                cv2.putText(
                    frame,
                    'Sem depth',
                    (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

        #exibe a imagem RGB com a profundidade
        cv2.imshow(
            'RealSense RGB + Depth',
            frame
        )
        cv2.waitKey(1)

#funcao principal
def main(args=None):
    
    rclpy.init(args=args)

    node = CameraDepthNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()


if __name__ == '__main__':
    main()