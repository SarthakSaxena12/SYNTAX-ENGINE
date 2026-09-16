from setuptools import setup, find_packages

setup(
    name='markdown-engine-pro',
    version='1.0.0',
    description='A highly scalable, extensible Markdown-to-HTML parser using only standard library',
    author='SS',
    py_modules=['main', 'parser', 'rules'],
    entry_points={
        'console_scripts': [
            'md-engine=main:main',
        ],
    },
    python_requires='>=3.8',
)
