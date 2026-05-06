from setuptools import find_packages, setup

package_name = 'lidar_pipeline'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'lidar_simulator = lidar_pipeline.lidar_simulator:main',
            'point_filter = lidar_pipeline.point_filter:main',
            'cone_detector = lidar_pipeline.cone_detector:main',
            'decision_node = lidar_pipeline.decision_node:main',
        ],
    },
)
