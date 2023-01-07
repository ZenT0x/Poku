#!/bin/bash
screen -S serveur -X stuff "`echo -ne \"restart\r\"`"