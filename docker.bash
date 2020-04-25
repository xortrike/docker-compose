#!/bin/bash

declare -A projects
projects=(
	[1]="Magento 2:/home/user/projects/magento2/docker"
)

function RenderProjects
{
	clear
	local CLREOL=$'\x1B[K'
	echo -e "\e[48;5;4m            \e[1m\e[97mDocker - Projects${CLREOL}\e[0m\e[49m"
	echo ""
	for index in "${!projects[@]}"
	do
		IFS=":" read -r -a buffer <<< "${projects[$index]}"
		# echo ${buffer[0]}" = "${buffer[1]}
		printf "%3d - %s\n" $index "${buffer[0]}"
	done
	echo ""
}

function StartProject
{
	if [[ ! -z ${projects[$1]} ]]
	then
		clear
		IFS=":" read -r -a buffer <<< "${projects[$1]}"
		docker-compose --project-directory "${buffer[1]}" --file "${buffer[1]}/docker-compose.yml" up -d
		ShowContainers "$1"
	fi
}

function StopProject
{
	if [[ ! -z ${projects[$1]} ]]
	then
		clear
		IFS=":" read -r -a buffer <<< "${projects[$1]}"
		docker-compose --project-directory "${buffer[1]}" --file "${buffer[1]}/docker-compose.yml" stop
	fi
}

function ShowContainers
{
	local containers=($(docker container ls --format "{{.Names}}"))
	local count=$(expr ${#containers[@]} + 1)

	local container=""

	while [[ $container != "0" ]]
	do
		clear
		local CLREOL=$'\x1B[K'
		echo -e "\e[48;5;4m            \e[1m\e[97mDocker - Containers${CLREOL}\e[0m\e[49m"
		echo ""
		for i in "${!containers[@]}"
		do
			printf "%3d - %s\n" $(expr $i + 1) ${containers[$i]}
		done
		echo ""
		read -p "Enter menu number: " container

		if [[ $container > 0 && $container < $count ]]
		then
			clear
			i=$(expr $container - 1)
			docker exec -it ${containers[$i]} bash
		fi
	done

	StopProject "$1"
}

# Project
project=""

while [[ $project != "0" ]]
do
	# Render Projects
	RenderProjects

	read -p "Enter menu number: " project

	if [[ ! -z "$project" && "$project" != "0" ]]
	then
		StartProject "$project"
	fi
done

echo "Bye Docker Projects"
