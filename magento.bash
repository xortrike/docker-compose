#!/bin/bash

declare -A SIZE_CLI=(
	# [app]=3
)

declare -A MAGENTO_CLI=(
	# [app,1]="app:config:dump;Create dump of application"
	# [app,2]="app:config:import;Import data from shared configuration files to appropriate data storage"
	# [app,3]="app:config:status;Checks if config propagation requires update"
)

# Empty array for full allow
declare -a FILTER_CLI=(
	# "app"
	# "cache"
	# "catalog"
	# "cron"
	# "deploy"
	# "indexer"
	# "module"
	# "setup"
)

# Default CLI title
declare DEFAULT_TITLE="Magento 2 - Terminal"

# Create Magento 2 commads list
function ReadCommandsList
{
	echo -e "\e[32mReading commands list...\e[0m"

	local i=0
	local currentType=""
	IFS=$'\n'

	for line in $(php bin/magento list)    
	do
		((i+=1))
		# Get CLI version
		if (( $i == 1 ))
		then
			if [[ ! -z $line ]]
			then
				DEFAULT_TITLE=$line
			fi
		fi
		# Skip header text
		if (( $i < 15 ))
		then
			continue
		fi
		# Read and write data
		if [[ ${line:0:2} == "  " && ! -z $currentType ]]
		then
			((SIZE_CLI[$currentType]+=1))
			index=${SIZE_CLI[$currentType]}
			MAGENTO_CLI[$currentType,$index]=$(echo "${line:2}" | sed -e 's/  \+/;/g')
		else
			currentType=${line:1}
			# Skip exclude
			if [[ ! -z "$FILTER_CLI" && ! " ${FILTER_CLI[@]} " =~ " ${currentType} " ]]; then
				currentType=""
				continue
			fi
			SIZE_CLI[$currentType]=0
		fi
	done
}

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
	echo -e "\e[48;5;202m            \e[1m\e[97m${DEFAULT_TITLE} - $PWD${CLREOL}\e[0m\e[49m\n"
    for key in ${!SIZE_CLI[@]}
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
	if (( ${SIZE_CLI[$1]} > 10 )); then
		n=2
	fi

    for (( i=1; i<=${SIZE_CLI[$1]}; i++ ))
    do
        IFS=";" read -r -a data <<< "${MAGENTO_CLI[$1,$i]}"
        if [[ -z ${data[1]} ]]
		then
			printf "%8d.%${n}d - %s\n" $index $i ${data[0]}
		else
			printf "%8d.%${n}d - %-44s%s\n" $index $i ${data[0]} "${data[1]}"
		fi
    done
}

function RunCommandLine
{
	local args=$@

	# Save last command
	if [[ $args != "l" ]]; then
		LAST_COMMANDS="$args"
	fi

	IFS=";" read -r -a multiple <<< "$args"
	if [[ ${#multiple[@]} > 1 ]]
	then
		for codes in "${multiple[@]}"
		do
			MagentoCommandLine "$codes"
			CustomCommandLine "$codes"
		done
	else
		MagentoCommandLine "$args"
		CustomCommandLine "$args"
	fi

    # Skip pause for open sub category
    if [[ ! -z "$work" ]]
    then
        pause
    fi
}

function CustomCommandLine
{
	if [[ $1 == "--help" ]]; then
		HelpInformation
    elif [[ $1 == "p" ]]; then
        echo "Set permission..."
        chmod -R 775 .
		echo "Set group..."
        chown -R www-data:1001 .
        work="1"
	elif [[ $1 == "l" ]]; then
		RunCommandLine "$LAST_COMMANDS"
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
    for key in ${!SIZE_CLI[@]}
    do
        if [[ $i == $type ]]
		then
			type=$key
		fi
        ((i+=1))
    done

	# Command line
	if [[ -z ${MAGENTO_CLI[$type,$index]} ]]
	then
		return 0
	fi

	# Get command
    IFS=";" read -r -a buffer <<< "${MAGENTO_CLI[$type,$index]}"
	command=${buffer[0]}

	echo -e "\e[93m => $codes [$command] [$params]\e[0m"
	if [[ -f "$bin" ]]; then
		php $bin $command $params
        work="1"
	fi
}

function HelpInformation
{
	clear
	local CLREOL=$'\x1B[K'
	echo -e "\e[48;5;202m            \e[1m\e[97mAdditionally Params${CLREOL}\e[0m\e[49m\n"
	echo "  + - Add plus for set params."
	echo "  ; - Use semicolon for run multi commands."
	echo "  p - Set project permissions."
	echo "  l - Run the last commands."

	pause
}

# Reading commands list if default commands list is empty
if [[ -z ${SIZE_CLI[@]} && -z ${MAGENTO_CLI[@]} ]]
then
	ReadCommandsList
fi

# Global variables
menu=""
work=""
LAST_COMMANDS=""

while [[ $menu != "0" ]]
do
    work=""
	RenderMenu $menu
	read -p "Enter Number: " menu

	if [[ ! -z "$menu" && "$menu" != "0" ]]
	then
		RunCommandLine "$menu"
	fi
done

clear
echo -e "\e[32mMagento CLI closed.\e[0m"
