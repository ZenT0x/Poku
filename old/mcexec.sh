#!/bin/bash
screen -S serveur -X stuff "`echo -ne \""$1"\r\"`"
