wget http://dl.fedoraproject.org/pub/fedora/linux/releases/26/Everything/x86_64/os/Packages/l/libpng15-1.5.28-2.fc26.x86_64.rpm
sudo yum install -y libpng15-1.5.28-2.fc26.x86_64.rpm
rm libpng15-1.5.28-2.fc26.x86_64.rpm
sudo rpm --import "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF"
sudo yum-config-manager --add-repo http://download.mono-project.com/repo/centos/
sudo yum install -y mono