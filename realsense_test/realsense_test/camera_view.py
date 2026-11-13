#No ROS 2 para visualizacao da imagem RGB da RealSense

#Este programa se inscreve no topico de imagem colorida publicado pela realsense, 
#recebe as imagens no formato utilizado pelo ROS 2, converte essas mensagens para o formato do OpenCV utilizando CvBridge 
#e exibe a imagem em tempo real em uma janela

#Fluxo geral:
#RealSense -> topico ROS 2 -> subscriber -> CvBridge -> OpenCV -> janela



#biblioteca que permite escrever nos do ROS2 em python
import rclpy 
from rclpy.node import Node

#tipo de mensagem utilizado pelo ROS2 para transmitir imagens
from sensor_msgs.msg import Image

#responsavel por converter imagens do formato ROS para OpenCV
from cv_bridge import CvBridge

import cv2


#No responsavel por receber e exibir a imagem RGB da realsense
#O no se inscreve no topico de imagem colorida publicado pelo driver realsense2_camera e converte cada 
#mensagem recebida para uma imagem compativel com OpenCV.
class CameraNode(Node):
    
    def __init__(self):
        #inicializa o no ROS2 com o nome "camera_node"
        super().__init__('camera_node')

        #cria a ponte entre imagens ROS e imagens utilizadas pelo OpenCV
        self.bridge = CvBridge()


        # Cria uma inscricao no topico de imagem RGB da RealSense.
        #
        # Parametros:
        #   Image: tipo da mensagem recebida
        #   topico: onde a RealSense publica a imagem RGB
        #   image_callback: funcao chamada sempre que chega uma nova imagem
        #   10: tamanho da fila de mensagens
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10
        )

        self.get_logger().info('Esperando imagem da RealSense...')

    #funcao executada toda vez que uma nova imagem RGB for recebida
    def image_callback(self, msg):

        #converte a imagem do formato ROS para uma matriz OpenCV
        #bgr8 e o formato padrao utilizado pelo OpenCV: blue, green, red, com 8 bits por canal
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        #mostra a imagem em uma janela
        cv2.imshow('RealSense RGB', frame)

        #permite que o opencv atualize a janela
        cv2.waitKey(1)


#funcao principal do no
def main(args=None):

    #inicializa o ROS2 para o processo
    rclpy.init(args=args)

    #cria uma instancia do no
    node = CameraNode()

    try:
        #mantem o no executando e processando callbacks
        rclpy.spin(node)

    except KeyboardInterrupt:
        #para encerrar o programa com ctrl+c sem erro    
        pass
    
    finally:

        #libera os recursos utilizados pelo no
        node.destroy_node()

        #fecha as janelas criadas pelo opencv
        cv2.destroyAllWindows()

        #finaliza a comunicacao com o ROS2
        rclpy.shutdown()


if __name__ == '__main__':
    main()