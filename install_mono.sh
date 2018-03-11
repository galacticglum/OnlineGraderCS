sudo mkdir -p /tmp/mono_dependencies
sudo cd /tmp/mono_dependencies
sudo wget http://dl.fedoraproject.org/pub/fedora/linux/development/rawhide/Everything/x86_64/os/Packages/l/libpng15-1.5.30-3.fc28.x86_64.rpm
sudo yum install -y libpng15-1.5.30-3.fc28.x86_64.rpm
sudo yum install yum-utils
sudo rpm --import "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF"
sudo yum-config-manager --add-repo http://download.mono-project.com/repo/centos/
sudo yum clean all
sudo yum makecache
sudo yum install mono-devel -y
sudo rm -rf /tmp/mono_dependencies