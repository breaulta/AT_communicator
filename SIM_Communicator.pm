package SIM_Communicator;

use strict;
use warnings;

#sim card / communicator class
sub new {
	my $class = shift;
	my $self = {@_};
	bless $self, $class;
	return $self;
}

#Pull from python script using AT commands and return array of unread SMS objects.
sub get_unread_texts {
	#pull from python
	#put into array of sms objects

	#Array of unread SMS objects to return.
	my @unread_texts;

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

			#Now that we've extracted text fields, put them in SMS object.
			my $sms = SMS->new(
				index => $index,
				status => $status,
				phone => $phone,
				date => $date,
				message => $message
			);
			push @unread_texts, $sms;
		}
	}
	return @unread_texts;
}





package SMS;

sub new {
	my $class = shift;
	my $self = {@_};
	bless $self, $class;
	return $self;
}

sub index { $_[0]->{index}=$_[1] if defined $_[1]; return $_[0]->{index} }
sub status { $_[0]->{status}=$_[1] if defined $_[1]; return $_[0]->{status} }
sub phone { $_[0]->{phone}=$_[1] if defined $_[1]; return $_[0]->{phone} }
sub date { $_[0]->{date}=$_[1] if defined $_[1]; return $_[0]->{date} }
sub message { $_[0]->{message}=$_[1] if defined $_[1]; return $_[0]->{message} }

1;
