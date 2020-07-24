#!/bin/bash

function CreateDirectory
{
	local dir=$1
	local directory=(
		[0]="docker"
		[1]="logs"
		[2]="logs/apache"
		[3]="logs/mysql"
		[4]="mysql"
		[5]="mysql/data"
		[6]="mysql/dump"
		[7]="www"
	)
	local permission=(
		[0]=""
		[1]="docker"
		[2]="docker"
		[3]="docker"
		[4]="docker"
		[5]="docker"
		[6]="docker"
		[7]="www-data"
	)
	for i in "${!directory[@]}"
	do
		if [ -d "${dir}/${directory[$i]}" ]
		then
			echo "Directory skip: ${directory[$i]}"
		else
			echo "Create directory: ${directory[$i]}"
			mkdir -p "${dir}/${directory[$i]}"
			if [[ ! -z ${permission[$i]} ]]
			then
				sudo chmod -R 775 "${dir}/${directory[$i]}"
				sudo chown -R $USER:${permission[$i]} "${dir}/${directory[$i]}"
			fi
		fi
	done

	touch "${dir}/logs/apache/access.log"
	touch "${dir}/logs/apache/error.log"
	sudo chmod -R 775 "${dir}/logs/apache/*"
	sudo chown -R $USER:docker "${dir}/logs/apache/*"
}

function setCertificate
{
	cd ${path}"/docker/apache/openssl"

	if [ -z "$1" ]; then
		echo "Please supply a subdomain to create a certificate for";
		echo "e.g. mysite.localhost"
		exit;
	fi

	if [ -f device.key ]; then
		KEY_OPT="-key"
	else
		KEY_OPT="-keyout"
	fi

	DOMAIN=$1
	COMMON_NAME=${2:-$1}

	if [ -f $DOMAIN ]; then
		rm -rf $DOMAIN
	fi

	SUBJECT="/C=CA/ST=None/L=NB/O=None/CN=$COMMON_NAME"
	NUM_OF_DAYS=999

	openssl req -new -newkey rsa:2048 -sha256 -nodes $KEY_OPT device.key -subj "$SUBJECT" -out device.csr

	cat v3.ext | sed s/%%DOMAIN%%/$COMMON_NAME/g > /tmp/__v3.ext

	openssl x509 -req -in device.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out device.crt -days $NUM_OF_DAYS -sha256 -extfile /tmp/__v3.ext

	mkdir $DOMAIN

	mv device.csr $DOMAIN/certificate-chain-file.csr
	mv device.crt $DOMAIN/certificate-file.crt
	cp device.key $DOMAIN/certificate-key-file.key

	if [ ! -f "../cert" ]; then
		mkdir -p "../cert"
	fi
	mv $DOMAIN "../cert"
	cd ${path}
}

path=$PWD
name="docker.tar.bz2"
buffer=""

# Install
declare -A config
config["project_name"]=${PWD##*/}
config["host_name"]="example.local"

# Project Name
read -p "Enter Project name [${config["project_name"]}]:" buffer
if [ ! -z $buffer ]; then
	config["project_name"]=$buffer
fi

# Site Address
read -p "Enter Site Address [${config["host_name"]}]:" buffer
if [ ! -z $buffer ]; then
	config["host_name"]=$buffer
fi

# Before start install
echo "Everything is ready for installation."
echo " - Project Name: ${config["project_name"]}"
echo " - Site Address: ${config["host_name"]}"
read -p "Start to install? [y/n]: " buffer
if [ -z $buffer ] || [ $buffer != "y" ]; then
	exit
fi



echo -e "\nInstalling..."
# Step 1 - Create Directory
CreateDirectory $path

# Step 2 - Extract Archive
if [ ! -f "${path}/${name}" ]; then
	echo "Error! Archive ${name} not found."
	exit
fi
tar xvC "${path}/docker" -f "${path}/${name}"

# Step 3 - SSL sertifacation
setCertificate ${config["host_name"]}

# Step 4 - Configuration
search="example.local"
replace=${config["host_name"]}
sed -i "s/${search}/${replace}/g" "${path}/docker/apache/default.conf"

search="HOST_NAME=example.local"
replace="HOST_NAME=${config["host_name"]}"
sed -i "s/${search}/${replace}/g" "${path}/docker/.env"

search="COMPOSE_PROJECT_NAME=example"
replace="COMPOSE_PROJECT_NAME=${config["project_name"]}"
sed -i "s/${search}/${replace}/g" "${path}/docker/.env"

# Finish
rm -f "${path}/${name}"
rm -f "${path}/install.bash"
