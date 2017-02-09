#!/usr/bin/perl -w

###########################################################
# Program : create_tables.pl
# Purpose : Connects to a mysql server and executes SQL
#           statements stored in a file
# Author  : Anant Seethalakshmi
###########################################################
use strict;
use DBI;        # import the DBI module
use DBD::mysql; # import the DB drivers for mysql

# connect to the database perl_test
my $dbh = DBI-> connect("dbi:mysql:perl_test","any",);  


my $sql_statement; #scalar used to hold the sql statement

# Open the file that holds the sql statements in read more
open(FH,'<','./create_tables.sql') or die $!;

# loop through each line and execute the sql statement
while(<FH>)
{
	$sql_statement = $_;
	next if $_ =~ /^\#/;
	my $statement_handle = $dbh->prepare($sql_statement);
	
	# execute the sql statements
	$statement_handle->execute;
	print ( "$_\n");
}