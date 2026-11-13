#Arquivo de configuracao do pacote ROS 2 realsense_test

#Este arquivo define como o pacote Python sera instalado pelo sistema de build do ROS 2, 
#quais arquivos fazem parte do pacote e quais executaveis podem ser chamados atraves do comando ros2 run.

from setuptools import find_packages, setup

#pacote de ROS2
package_name = 'realsense_test'

setup(
    name=package_name,
    version='0.0.0',

    #localiza os modulos pythons pertencentes ao pacote
    packages=find_packages(exclude=['test']),
    
    #arquivos necessarios para que o ROS2 reconheca o pacote
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],

    #dependencias necessarias para a instalacao do pacote python
    install_requires=['setuptools'],
    zip_safe=True,

    #informacoes do responsavel pelo pacote
    maintainer='beatriz',
    maintainer_email='beatrizslcosimatti@gmail.com',

    #informacoes gerais do pacote
    description='Pacote para testes e integracao da RealSense com ROS 2',
    license='TODO: License declaration',
    
    #dependencias utilizadas nos testes automaticos
    extras_require={
        'test': [
            'pytest',
        ],
    },

    #define os executaveis que poderao ser chamados com "ros2 run"
    entry_points={
        'console_scripts': [

            # Permite executar:
            #
            # ros2 run realsense_test camera
            #
            # O ROS vai executar a funcao main() localizada em: realsense_test/camera_view.py
            'camera = realsense_test.camera_view:main',

            # ros2 run realsense_test camera_depth
            'camera_depth = realsense_test.camera_depth:main',
        ],
    },
)
