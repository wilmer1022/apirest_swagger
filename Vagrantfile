
#tres maquinas virtuales:				nombre			descripcion
#VM1: centoserverador de carga				<centoserver>		nginx
#VM2: web						 		<servidor2>		httpd
#VM3: web						 		<servidor3>		httpd

Vagrant.configure("2") do |config|
	if Vagrant.has_plugin? "vagrant-vbguest"
		config.vbguest.no_install  = true
		config.vbguest.auto_update = false
		config.vbguest.no_remote   = true
	end
	config.vm.define :centoserver do |centoserver|
		centoserver.vm.box = "bento/centos-7.8"
		centoserver.vm.network :private_network, ip: "192.168.50.3"
		centoserver.vm.provision "shell", path: "script.sh"
		centoserver.vm.provision "file", source: "apirest", destination: "/home/vagrant/apirest"
		centoserver.vm.hostname = "centoserver"
		centoserver.vm.provider "virtualbox" do |v|
			v.name = "CentosFlaskSwagger"
			v.memory = 2048
			v.cpus = 2
		end
	end
end

