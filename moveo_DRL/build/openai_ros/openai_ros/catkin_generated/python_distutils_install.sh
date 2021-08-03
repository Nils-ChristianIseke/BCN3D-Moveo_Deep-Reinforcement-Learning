#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/src/openai_ros/openai_ros"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/install/lib/python3/dist-packages:/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/build" \
    "/home/nils/anaconda3/bin/python3" \
    "/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/src/openai_ros/openai_ros/setup.py" \
     \
    build --build-base "/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/build/openai_ros/openai_ros" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/install" --install-scripts="/home/nils/Documents/Studium/Bachelorarbeit/praktischer_Teil/moveo_DRL/install/bin"
