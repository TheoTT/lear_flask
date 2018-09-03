from setuptools import find_packages, setup

setup(
    name='blogApp',
    version='1.0.0',
    packages=find_packages(),#packages 告诉 Python 包所包括的文件夹（及其所包含的 Python 文件）find_packages() 自动找到这些文件夹
    include_package_data=True,#包含其他文件夹，如静态文件和模板文件所在的文件夹
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)