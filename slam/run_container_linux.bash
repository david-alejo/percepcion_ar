
xhost +local:docker

mkdir -p $HOME/percepcion_ar_shared
docker run -it \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --name rssa \
    --net=host \
    --privileged \
    --mount type=bind,source=$HOME/percepcion_ar_shared,target=/home/percepcion_ar \
    rssa \
    bash
    
docker rm percepcion_ar
