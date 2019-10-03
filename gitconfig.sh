#!/bin/bash

for i in "$@"
do
case $i in
    -c|--create)
    echo "--creating--"
    git config --global user.name iliaeg
    git config --global user.email egorovilyak@yandex.ru
    shift # past argument=value
    ;;
    -r|--remove)
    echo "--removing--"
    git config --global --unset-all user.name
    git config --global --unset-all user.email
    shift # past argument=value
    ;;
    -i|--info)
    echo "--info--"
    git config --global --list
    shift # past argument=value
    ;;
    -h|--help)
    echo "Usage: ./gitconfig.sh [-c|--create] [-r|--remove] [-i|--info] [-h|--help]"
    shift # past argument=value
    ;;
    # --default)
    # DEFAULT=YES
    # shift # past argument with no value
    # ;;
    *)
          # unknown option
    ;;
esac
done
 
