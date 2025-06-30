conda env create -f TiTok3D.yml --name TiTok3D    
conda run -n TiTok3D pip install git+https://github.com/nottombrown/imagenet_stubs
conda run -n TiTok3D pip show imagenet_stubs