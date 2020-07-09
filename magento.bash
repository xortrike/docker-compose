#!/bin/bash

# How add new group?
# Add group to array [types] where key "group key" and value "group name".
# Add group key to array [sort].

# How add new command?
# Add group to array [size] where key "group name" and value "count group command".
# Add group command to array [magento] where key "group key, command key".
# Argument for run command "exec", show description "desc".

# IFS=';' read -ra ADDR <<< "$IN"

declare -A types
types=(
	[2]=app
	[3]=cache
	[4]=catalog
	[6]=cron
	[8]=deploy
	[12]=indexer
	[17]=module
	[22]=setup
)
sort=(2 3 4 6 8 12 17 22)

# Last ID in magento array
declare -A size
size=(
	[app]=3
	[cache]=5
	[catalog]=2
	[cron]=3
	[deploy]=2
	[indexer]=8
	[module]=4
	[setup]=16
)

declare -A magento
# magento=(
# 	[app,1]="app:config:dump+Create dump of application"
# 	[app,2]="app:config:import+Import data from shared configuration files to appropriate data storage"
# 	[app,3]="app:config:status+Checks if config propagation requires update"
# )
magento=(
	# app
	[2,1,exec]="app:config:dump"
	[2,1,desc]="Create dump of application"
	[2,2,exec]="app:config:import"
	[2,2,desc]="Import data from shared configuration files to appropriate data storage"
	[2,3,exec]="app:config:status"
	[2,3,desc]="Checks if config propagation requires update"
	# cache
	[3,1,exec]="cache:clean"
	[3,1,desc]="Cleans cache type(s)"
	[3,2,exec]="cache:disable"
	[3,2,desc]="Disables cache type(s)"
	[3,3,exec]="cache:enable"
	[3,3,desc]="Enables cache type(s)"
	[3,4,exec]="cache:flush"
	[3,4,desc]="Flushes cache storage used by cache type(s)"
	[3,5,exec]="cache:status"
	[3,5,desc]="Checks cache status"
	# catalog
	[4,1,exec]="catalog:images:resize"
	[4,1,desc]="Creates resized product images"
	[4,2,exec]="catalog:product:attributes:cleanup"
	[4,2,desc]="Removes unused product attributes."
	# Cron
	[6,1,exec]="cron:install"
	[6,1,desc]="Generates and installs crontab for current user"
	[6,2,exec]="cron:remove"
	[6,2,desc]="Removes tasks from crontab"
	[6,3,exec]="cron:run"
	[6,3,desc]="Runs jobs by schedule"
	# deploy
	[8,1,exec]="deploy:mode:set"
	[8,1,desc]="Set application mode."
	[8,2,exec]="deploy:mode:show"
	[8,2,desc]="Displays current application mode."
	# indexer
	[12,1,exec]="indexer:info"
	[12,1,desc]="Shows allowed Indexers"
	[12,2,exec]="indexer:reindex"
	[12,2,desc]="Reindexes Data"
	[12,3,exec]="indexer:reset"
	[12,3,desc]="Resets indexer status to invalid"
	[12,8,exec]="indexer:status"
	[12,8,desc]="Shows status of Indexer"
	# module
	[17,1,exec]="module:disable"
	[17,2,exec]="module:enable"
	[17,3,exec]="module:status"
	[17,4,exec]="module:uninstall"
	# setup
	[22,9,exec]="setup:di:compile"
	[22,13,exec]="setup:static-content:deploy"
	[22,16,exec]="setup:upgrade"
)

function pause
{
	echo ""
	read -p "Press [Enter] key to continue..."
	echo ""
}

function RenderMenu
{
	clear
	local CLREOL=$'\x1B[K'
	echo -e "\e[48;5;202m            \e[1m\e[97mMagento 2 - Terminal${CLREOL}\e[0m\e[49m"
	# printf "\n\tMagento 2 - Terminal\n\n"
	# Applay custom sort because ${!types[@]}
	echo ""
	# local sort=(3 17 22)
	for index in ${sort[@]}
	do
		printf "%3d - %s\n" $index ${types[$index]}
		if [[ $1 == $index ]]
		then
			RenderSubMenu $index
		fi
	done
	echo ""
}

function RenderSubMenu
{
	index=$1
	type=${types[$index]}
	for (( i=1; i<=${size[$type]}; i++ ))
	do
		# Skip commant if not exists
		if [[ -z ${magento[$index,$i,exec]} ]]
		then
			continue
		fi
		# Show description if exists
		if [[ -z ${magento[$index,$i,desc]} ]]
		then
			printf "%8d.%2d - %s\n" $index $i ${magento[$index,$i,exec]}
		else
			printf "%8d.%d - %-44s%s\n" $index $i ${magento[$index,$i,exec]} "${magento[$index,$i,desc]}"
		fi
	done
}

function MagentoCommandLine
{
	local args=$@
	local bin="$PWD/bin/magento"
	local codes=${args%%+*}
	local params=""

	if [[ $args == *"+"* ]]; then
		params=${args#*+}
	fi

	IFS="." read -r -a code <<< "$codes"
	type=${code[0]}
	index=${code[1]}
	command=${magento[$type,$index,exec]}
	#echo "Run: [$command] [$params]"

	echo -e "\e[93m => $codes [$command] [$params]\e[0m"
	if [[ -f "$bin" ]]; then
		php $bin $command $params
	fi
}

# For exit, enter zero
# Add plus for arguments

# Menu
menu=""

while [[ $menu != "0" ]]
do
	# Render menu items
	RenderMenu $menu

	read -p "Enter menu number: " menu

	# if [[ -z "$menu" =~ ^[0-9]+$ ]]

	if [[ ! -z "$menu" && "$menu" != "0" ]]
	then
		# Access
		if [[ $menu == "p" ]]
		then
			chmod -R 775 .
			chown -R www-data:1001 .
			continue
		fi
		clear
		IFS=";" read -r -a points <<< "$menu"
		for point in "${points[@]}"
		do
			if [[ $menu == *"."* ]]
			then
				MagentoCommandLine "$point"
			fi
		done
		# Pause
		if [[ $menu == *"."* ]]
		then
			pause
		fi
	fi
done

echo "Bye Magento Terminal"
