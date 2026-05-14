xhost +local:docker 2>/dev/null || true

mkdir -p $HOME/rssa_shared

docker run -it \
    --env="DISPLAY=$DISPLAY" \
    --env="WAYLAND_DISPLAY=$WAYLAND_DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="XDG_RUNTIME_DIR=/tmp/runtime" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="/mnt/wslg:/mnt/wslg" \
    --volume="/run/user/1000/wayland-0:/tmp/runtime/wayland-0" \
    --name rssa \
    --net=host \
    --privileged \
    --mount type=bind,source=$HOME/rssa_shared,target=/home/rssa \
    rssa \
    bash

docker rm rssa
