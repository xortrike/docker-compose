#!/bin/bash

function CreateDirectory
{
	local dir=$1
	local directory=(
		"docker"
		"logs/nginx"
		"logs/mysql"
		"mysql/data"
		"mysql/dump"
		"www"
	)
	for dirname in "${directory[@]}"
	do
		if [ -d "${dir}/${dirname}" ]
		then
			echo "Directory skip: ${dirname}"
		else
			echo "Creating directory: ${dirname}"
			mkdir -p "${dir}/${dirname}"
		fi
	done
}

function setCertificate
{
	cd ${path}"/docker/nginx/openssl"

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

	mv device.csr $DOMAIN/$DOMAIN.csr
	mv device.crt $DOMAIN/$DOMAIN.crt
	cp device.key $DOMAIN/$DOMAIN.key

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
config["user_name"]=$USER
config["user_id"]=$UID

# Project Name
read -p "Enter project name [${config["project_name"]}]: " buffer
if [ ! -z $buffer ]; then
	config["project_name"]=$buffer
fi

# Site Address
read -p "Enter local site address [${config["host_name"]}]: " buffer
if [ ! -z $buffer ]; then
	config["host_name"]=$buffer
fi

# User Name
read -p "Enter local user name [${config["user_name"]}]: " buffer
if [ ! -z $buffer ]; then
	config["user_name"]=$buffer
fi

# User ID
read -p "Enter local user ID [${config["user_id"]}]: " buffer
if [ ! -z $buffer ]; then
	config["user_id"]=$buffer
fi

# Before start install
echo -e "\nEverything is ready for installation."
echo " - Project Name: ${config["project_name"]}"
echo " - Site Address: ${config["host_name"]}"
echo " - User Name:    ${config["user_name"]}"
echo " - User ID:      ${config["user_id"]}"
read -p "Start to install? [y/n]: " buffer
if [ -z $buffer ] || [ $buffer != "y" ]; then
	exit
fi



echo -e "\nInstalling..."
# Step 1 - Create Directory
CreateDirectory $path

# Step 2 - Extract Archive
if [[ ! -f "${path}/${name}" ]]; then
	echo "Error! Archive ${name} not found."
	exit
fi
tar xvC "${path}/docker" -f "${path}/${name}"

# Step 3 - SSL sertifacation
setCertificate ${config["host_name"]}

# Step 4 - Configuration
search="example.local"
replace=${config["host_name"]}
sed -i "s/${search}/${replace}/g" "${path}/docker/nginx/magento.conf"
sed -i "s/${search}/${replace}/g" "${path}/docker/nginx/joomla.conf"

search="HOST_NAME=example.local"
replace="HOST_NAME=${config["host_name"]}"
sed -i "s/${search}/${replace}/g" "${path}/docker/.env"

search="COMPOSE_PROJECT_NAME=example"
replace="COMPOSE_PROJECT_NAME=${config["project_name"]}"
sed -i "s/${search}/${replace}/g" "${path}/docker/.env"

search="WEB_USER_NAME=username"
replace="WEB_USER_NAME=${config["user_name"]}"
sed -i "s/${search}/${replace}/g" "${path}/docker/.env"

search="WEB_USER_ID=userid"
replace="WEB_USER_ID=${config["user_id"]}"
sed -i "s/${search}/${replace}/g" "${path}/docker/.env"

# Finish
rm -f "${path}/${name}"
rm -f "${path}/install.bash"
