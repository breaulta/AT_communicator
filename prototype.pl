#!/usr/bin/perl
use warnings;
use strict;

#Send and receive texts with sms perl package.

use SMS;

my $sim_card = Transmitter->new();
my $sms = SMS->new();

#create array of SMS objects
my @unread_texts = $sim_card->get_unread_texts();
foreach $message (@unread_texts){
	print $message->date();
	print $message->number();
	print $message->content();
}

#Send text message.
$sms = SMS->new(
	type => "outgoing"
	phone => "5033803136",
	message => "hi how are you?"
);
$sms->send();
