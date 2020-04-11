#script by Robin Newman to build Sonic Pi 3.2.0 release on Raspbian Buster 2020-02-05
# #version 3 with correct build of erlang beam files included
 SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
 SOURCE_DIR=$SCRIPT_DIR/sp
# echo $SCRIPT_DIR
# echo $SOURCE_DIR

mkdir -p $SOURCE_DIR
cd $SOURCE_DIR
# #wget https://github.com/samaaron/sonic-pi/archive/v3.2.0.tar.gz
# #tar -zxf v3.2.0.tar.gz
git clone https://github.com/samaaron/sonic-pi.git
cp ../build-ubuntu-app.sh  $SOURCE_DIR/sonic-pi/app/gui/qt/
cd $SOURCE_DIR/sonic-pi/app/gui/qt/
chmod +x build-ubuntu-app.sh
sudo ./build-ubuntu-app.sh
# wget http://r.newman.ch/rpi/sp32RpiPatches.tar.gz
# echo "extracting Sonic Pi source.."
# tar -zxf v3.2.0.tar.gz
# echo "extracting patch scripts.."
# tar -zxf sp32RpiPatches.tar.gz
# extract install folder
# mv sp32RpiPatches/spInstall ./
# cd sp32RpiPatches
# echo "applying patches..."
# rsync -a qt/ ../sonic-pi-3.2.0/app/gui/qt/
# cd ../sonic-pi-3.2.0/app/gui/qt/

# echo "compiling vendor extensions..."
# ../../server/ruby/bin/compile-extensions.rb
# echo "running unix-prebuild script..."
# ./unix-prebuild.sh
# echo "build beam files.."
# cd ../../server/erlang
# /usr/bin/erlc osc.erl
# /usr/bin/erlc pi_server.erl.erl
# cd ../../gui/qt
# echo "running unix_config script..."
# ./unix-config.sh
# echo "building gui and sonic-pi app..."
# cd build
# cmake --build .
# echo "build complete"
