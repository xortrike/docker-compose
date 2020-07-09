#!/bin/bash

declare -a PROJECTS=(
	"Magento 2:/var/www/projects/magento/docker"
)

function RenderProjects
{
	clear
	local CLREOL=$'\x1B[K'
	echo -e "\e[48;5;4m            \e[1m\e[97mDocker - Projects${CLREOL}\e[0m\e[49m\n"
	for i in ${!PROJECTS[@]}
	do
		IFS=":" read -r -a buffer <<< "${PROJECTS[$i]}"
		printf "%3d - %s\n" $((i+1)) "${buffer[0]}"
	done
	echo ""
}

function StartProject
{
	if [[ ! -z ${PROJECTS[$1]} ]]
	then
		clear
		IFS=":" read -r -a buffer <<< "${PROJECTS[$1]}"
		docker-compose --project-directory "${buffer[1]}" --file "${buffer[1]}/docker-compose.yml" up -d
		RenderContainers "$1"
	fi
}

function StopProject
{
	if [[ ! -z ${PROJECTS[$1]} ]]
	then
		clear
		IFS=":" read -r -a buffer <<< "${PROJECTS[$1]}"
		docker-compose --project-directory "${buffer[1]}" --file "${buffer[1]}/docker-compose.yml" stop
	fi
}

function RenderContainers
{
	local containers=($(docker container ls --format "{{.Names}}"))
	local count=$(expr ${#containers[@]} + 1)
	local container=""

	while [[ $container != "0" ]]
	do
		clear
		local CLREOL=$'\x1B[K'
		echo -e "\e[48;5;4m            \e[1m\e[97mDocker - Containers${CLREOL}\e[0m\e[49m"

		IFS=":" read -ra buffer <<< "${PROJECTS[$1]}"
		echo -e "${buffer[0]}\n"

		for i in "${!containers[@]}"
		do
			printf "%3d - %s\n" $(expr $i + 1) ${containers[$i]}
		done
		echo ""
		read -p "Menu Number: " container

		if [[ $container > 0 && $container < $count ]]
		then
			clear
			i=$(expr $container - 1)
			docker exec -it ${containers[$i]} bash
		fi
	done

	StopProject "$1"
}

# Select Project Index
PROJECT=""

while [[ $PROJECT != "0" ]]
do
	RenderProjects
	read -p "Menu Number: " PROJECT

	if [[ ! -z "$PROJECT" && "$PROJECT" != "0" ]]
	then
		StartProject $(($PROJECT-1))
	fi
done

echo "Docker projects closed."
