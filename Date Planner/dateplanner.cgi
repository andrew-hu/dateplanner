#!/usr/bin/perl

use CGI qw (:standard);
use DBI;	# dbi = database interface
use DBD::mysql;	# dbd = database driver
# dbh = database handle
$dbh = DBI->connect("dbi:mysql:perl_test","gen6","gen6");
print header;

####################### MAIN PROGRAM #######################

	print ("<html><head>
		<link rel=\"stylesheet\" type=\"text/css\" href=\"dateplanner.css\" /> 
		<title>Date Planner</title></head><body>");
	
	print("<h1>Welcome to Date Planner!</h1><br>");

	print_desc();

######### EVENTS #########
	generate_events(); 

######### MOVIES #########

	generate_dinner(); 

######### DINNER #########

	generate_movies(); 

#############################################################

	print ("</body>"); 
	print ("</html>"); 

####################### SUBROUTINES #########################
sub generate_events {

	print "<div id=\"events\">";
	print("<h2>Events</h2><br>");


	$sth = $dbh->prepare("select * from gen62_events order by ID");
	$rv = $sth->execute;

	$count = 0;

	while( @rows = $sth->fetchrow_array) {
				$count++;
	}
	#print "count is $count<br>";
	$random = int(rand($count))+1;
	#print "random number is $random<br>";

	$sth = $dbh->prepare("select * from gen62_events where ID=$random");
	$rv = $sth->execute;

	while( @rows = $sth->fetchrow_array) {
		print " Plan an exciting day with your date and <i>$rows[1]</i>!<br><br>
				<img src=\"$rows[2]\" style=\"max-width:100%\";height:auto;><br><br>
				<i>$rows[3]</i><br>";
	} print "<br>";

	print "</div>";
}

sub generate_movies {
	print "<div id=\"movies\">";
	print("<h2>The Cinema</h2><br>");
		#Rotten Tomatoes key : 5j4tryswf6qfryehkerzb25m
	$sth = $dbh->prepare("select * from gen62_movie order by ID");
	$rv = $sth->execute;

	$count = 0;

	while( @rows = $sth->fetchrow_array) {
				$count++;
	}
	#print "count is $count<br>";
	$random = int(rand($count))+1;
	#print "random number is $random<br>";

	$sth = $dbh->prepare("select * from gen62_movie where ID=$random");
	$rv = $sth->execute;

	while( @rows = $sth->fetchrow_array) {
		print " You've finished dinner and you're looking for the perfect way
				to end your evening. It's too late to do anything too exhausting, but
				what about a relaxing night at the movies? <br><br>
				<i>Complete your perfect date with this critically
				acclaimed $rows[3] film at your favorite cinema!</i><br><br>
				<center><b>$rows[1]</b></center><br><br>
				<center><img src=\"$rows[2]\" style=\"max-width:50%\";height:auto;></center><br>
				<br>";
	} print "<br>";
	print "</div>";
}

sub generate_dinner {
	print "<div id=\"dinner\">";
	print("<h2>Cuisine</h2><br>");
		#Consumer Key		- iBJxmfq3iIQFtz7gTidR8Q
		#Consumer Secret	- 7O732L9aUuEsOl_PeBRhkxUczQ8
		#Token				- WymGrFO0NveKoirCrSI8yNbTnrEfZ1Fl
		#Token Secret		- OpbOiWON-jPzPgy9luNCpnifoys
	$sth = $dbh->prepare("select * from gen62_dinner order by ID");
	$rv = $sth->execute;

	$count = 0;

	while( @rows = $sth->fetchrow_array) {
				$count++;
	}
	#print "count is $count<br>";
	$random = int(rand($count))+1;
	#print "random number is $random<br>";

	$sth = $dbh->prepare("select * from gen62_dinner where ID=$random");
	$rv = $sth->execute;

	while( @rows = $sth->fetchrow_array) {
		print " It's supper time and you and your date are hungry from your adventures!<br><br>
				<i>In the mood for delicious $rows[4] food?</i><br><br>
				Have dinner at: <a href=\"$rows[3]\">$rows[1]!</a><br><br>
				<img src=\"$rows[2]\" style=\"max-width:100%\";height:auto;><br><br>
				<i>Guaranteed to be wicked scrumptious and to leave you satisfied!</i><br>
				<br>";
	} print "<br>";


	print "</div>";
}

sub print_desc {
	print "<div id=\"desc\">";
	print "<i>Looking to plan a date in Fremont but not sure 
	what to go? Planning a perfect evening for your special someone can 
	be a daunting task, but let's make it easier on you! Introducing the 
	Date Planner, your quick and simple guide for planning a date you won't 
	forget! No more looking on yelp for good food or googling ideas for your 
	first date: Date Planner has all the bases covered... all you have to do 
    is go on it!<br><br>
    If you would like Date Planner to give you another date plan, <u>simply refresh 
    the page</u>! <br><br>
    Have fun, and hope you enjoy!</i>";
    print "</div>";
}