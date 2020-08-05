#!/usr/bin/perl
use warnings;
use strict;

#Get texts with python script running AT+CMGL="ALL" AT command to SIM card.
open (my $query_texts, "-|", "python list_all_texts.py");

my $unread_texts = "";
while (my $line = <$query_texts>){
	$unread_texts .= $line;
}
my @messages = split('\+CMGL\: ', $unread_texts);
while (my $text = shift @messages){
	#Extract fields out of incoming sms.  /s = modifier that treats string as single line allowing '.' to match '\n'.
	if ($text =~ /^([0-9]+),\"([A-Z\s]+)\",\"\+?1?([0-9]{10})\",\"[^\"]*\",\"([^\"]+)\"\s+(.*)$/s){
		my $index = $1;
		my $status = $2;
		my $phone = $3;
		my $date = $4;
		my $message = $5;
		#If last message removing trailing 'OK' plus blank space characters.
		$message =~ s/(.*)([^\r\n]+)[\r\n]+OK.*/$1$2/s if scalar @messages == 0;
		#Remove carriages returns.
		$message =~ s/\r//g;
		#Remove trailing newlines.
		$message =~ s/(.*)[\n]+$/$1/s;
	}
}

