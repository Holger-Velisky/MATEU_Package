from distutils.core import setup
setup(
  name = 'MATEU',
  packages = ['MATEU'],
  version = 'v0.0.2',
  license='cc-by-sa-4.0',
  description = 'A fast chess library for chess engines development including an interface to play games with easy, efficient and short controls, simple piece-value evaluation, and a compressed python version of Mateu Chess Engine',
  author = 'Albert Mateu Carrasco',
  author_email = 'albertmateucarrasco@gmail.com',
  url = 'https://github.com/Holger-Velisky/MATEU_package',
  download_url = 'https://github.com/Holger-Velisky/MATEU_Package/archive/refs/tags/v0.0.2.tar.gz',    # I explain this later on
  keywords = ['CHESS', 'PYTHON', 'BOARD', 'GAMES', 'IA', 'ENGINE', 'MATEU', 'LICHESS', 'SOCKFISH', "ML","MULTIPROCESSING","DATA SCIENCE","FINANCE","CRYPTO","CYBERSECURITY","MULTIPURPOSE"],
  install_requires=[
          'chess',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Natural Language :: English',
    'License :: Free for non-commercial use',
    'Operating System :: POSIX',
    'Operating System :: Microsoft',
    'Operating System :: MacOS',
    'Operating System :: OS Independent',
    'Topic :: Utilities',
    'Topic :: Games/Entertainment :: Board Games',
    'Topic :: Games/Entertainment :: Real Time Strategy',
    'Topic :: Games/Entertainment :: Turn Based Strategy',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
  ],
)