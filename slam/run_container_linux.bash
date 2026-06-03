
xhost +local:docker

mkdir -p $HOME/percepcion_ar_shared
docker run -it \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --name percepcion_ar \
    --net=host \
    --privileged \
    --mount type=bind,source=$HOME/percepcion_ar_shared,target=/home/percepcion_ar \
    percepcion_ar \
    bash
    
docker rm percepcion_ar
