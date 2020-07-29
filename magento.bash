#!/bin/bash

name="Magento 2 - Terminal"
declare -A size
declare -A magento

# Empty array for full allow
declare -a allowed=(
	"app"
	"cache"
	"catalog"
	"cron"
	"deploy"
	"indexer"
	"module"
	"setup"
)

# Create Magento 2 commads list
i=0
currentType=""
IFS=$'\n'
for line in $(php bin/magento list)    
do
	((i+=1))
	# Get CLI version
	if (( $i == 1 ))
	then
		name=$line
	fi
	# Skip header text
	if (( $i < 15 ))
	then
		continue
	fi
	# Read and write data
	if [[ ${line:0:2} == "  " && ! -z $currentType ]]
	then
		((size[$currentType]+=1))
		index=${size[$currentType]}
		magento[$currentType,$index]=$(echo "${line:2}" | sed -e 's/  \+/;/g')
	else
		currentType=${line:1}
		# Skip exclude
		if [[ ! -z "$allowed" && ! " ${allowed[@]} " =~ " ${currentType} " ]]; then
			currentType=""
			continue
		fi
		size[$currentType]=0
	fi
done

declare -A size2=(
	[app]=3
	[cache]=5
	[catalog]=2
	[cron]=3
	[deploy]=2
	[indexer]=3
	[module]=4
	[setup]=3
)

declare -A magento2=(
	# app
	[app,1]="app:config:dump;Create dump of application"
	[app,2]="app:config:import;Import data from shared configuration files to appropriate data storage"
	[app,3]="app:config:status;Checks if config propagation requires update"
	# cache
	[cache,1]="cache:clean;Cleans cache type(s)"
	[cache,2]="cache:disable;Disables cache type(s)"
	[cache,3]="cache:enable;Enables cache type(s)"
	[cache,4]="cache:flush;Flushes cache storage used by cache type(s)"
	[cache,5]="cache:status;Checks cache status"
    # catalog
	[catalog,1]="catalog:images:resize;Creates resized product images"
	[catalog,2]="catalog:product:attributes:cleanup;Removes unused product attributes."
	# cron
	[cron,1]="cron:install;Generates and installs crontab for current user"
	[cron,2]="cron:remove;Removes tasks from crontab"
	[cron,3]="cron:run;Runs jobs by schedule"
	# deploy
	[deploy,1]="deploy:mode:set;Set application mode."
	[deploy,2]="deploy:mode:show;Displays current application mode."
	# indexer
	[indexer,1]="indexer:info;Shows allowed Indexers"
	[indexer,2]="indexer:reindex;Reindexes Data"
	[indexer,3]="indexer:reset;Resets indexer status to invalid"
	[indexer,4]="indexer:status;Shows status of Indexer"
	# module
	[module,1]="module:disable"
	[module,2]="module:enable"
	[module,3]="module:status"
	[module,4]="module:uninstall"
	# setup
	[setup,1]="setup:di:compile"
	[setup,2]="setup:static-content:deploy"
	[setup,3]="setup:upgrade"
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
    local index=1
	local CLREOL=$'\x1B[K'
	echo -e "\e[48;5;202m            \e[1m\e[97m${name} - $PWD${CLREOL}\e[0m\e[49m"
	echo ""
    for key in ${!size[@]}
    do
        printf "%3d - %s\n" $index $key
        if [[ $1 == $index ]]
		then
			RenderSubMenu $key
		fi
        ((index+=1))
    done
	echo ""
}

function RenderSubMenu
{
	local n=1
	if (( ${size[$1]} > 10 )); then
		n=2
	fi

    for (( i=1; i<=${size[$1]}; i++ ))
    do
        IFS=";" read -r -a data <<< "${magento[$1,$i]}"
        if [[ -z ${data[1]} ]]
		then
			printf "%8d.%${n}d - %s\n" $index $i ${data[0]}
		else
			printf "%8d.%${n}d - %-44s%s\n" $index $i ${data[0]} "${data[1]}"
		fi
    done
}

function CustomCommandLine
{
    if [[ $1 == "p" ]]
    then
        echo "Set permissions global..."
        chmod -R 775 .
        chown -R 1001:www-data .
        work="1"
    fi
}

function MagentoCommandLine
{
	local args=$@
	local bin="$PWD/bin/magento"
	local codes=${args%%+*}
	local params=""

	# Param
	if [[ $args == *"+"* ]]; then
		params=${args#*+}
	fi

    # Code
	IFS="." read -r -a code <<< "$codes"
    if [[ ${#code[@]} != 2 ]]
    then
        return 0
    fi
    type=${code[0]}
	index=${code[1]}

    # Type
    local i=1
    for key in ${!size[@]}
    do
        if [[ $i == $type ]]
		then
			type=$key
		fi
        ((i+=1))
    done

	# Command line
	if [[ -z ${magento[$type,$index]} ]]
	then
		return 0
	fi

	# Get command
    IFS=";" read -r -a buffer <<< "${magento[$type,$index]}"
	command=${buffer[0]}

	echo -e "\e[93m => $codes [$command] [$params]\e[0m"
	if [[ -f "$bin" ]]; then
		php $bin $command $params
        work="1"
	fi
}

# Global variables
menu=""
work=""

while [[ $menu != "0" ]]
do
    work=""
	RenderMenu $menu
	read -p "Enter menu number: " menu

	if [[ ! -z "$menu" && "$menu" != "0" ]]
	then
        IFS=";" read -r -a multiple <<< "$menu"
        if [[ ${#multiple[@]} > 1 ]]
        then
            for codes in "${multiple[@]}"
            do
                MagentoCommandLine "$codes"
                CustomCommandLine "$codes"
            done
        else
            MagentoCommandLine "$menu"
            CustomCommandLine "$menu"
        fi
        if [[ ! -z "$work" ]]
        then
            pause
        fi
	fi
done

echo "Bye Magento Terminal"
