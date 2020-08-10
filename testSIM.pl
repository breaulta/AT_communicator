#!/usr/bin/perl
use warnings;
use strict;

use lib ".";

use SIM_Communicator;

my $sim = SIM_Communicator->new();

my $sms = SMS->new( phone => 5033803136, message => "Aaron is a special guy :)" );
$sim->send_text($sms);



=pod
my @unread_texts = $sim->get_unread_texts();
foreach my $sms (@unread_texts) {
	print "index: ", $sms->index(), "\n";
	print "phone: ", $sms->phone(), "\n";
	print "message: ", $sms->message(), "\n";
	print "date: ", $sms->date(), "\n";
	print "status: ", $sms->status(), "\n";
}
