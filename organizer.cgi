#!/usr/bin/perl
# organizer.cgi
# 
# Adapted from the multimedia festival db: mm_projects.cgi, other programs
#  and Joy Hughes version of 'organizer.cgi', perl class spring 09


use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
print header;
#exit;


use DBI;
use DBD::mysql;

BEGIN {
     use CGI::Carp qw(carpout);
     open(LOG, ">>final_project_error.log") or
	        die("Unable to open mycgi-log: $!\n");
     carpout(LOG);
   }

# define necessary mysql vars, set up mysql connect
$database = "perl_test";
$dbh = DBI->connect("dbi:mysql:$database",,) or die ("dbi_connect: $DBI::errstr\n");

#print ("past opening the databalse $database\n<bbr>");
#exit;

######################################################################
# initialize a few things											##
# (some of these do not apply to this application)					##
######################################################################

$mailprog = "/usr/sbin/sendmail";


$| = 1;		#clear buffers	
my $url = "";
# Note below, $menu is pointer to an array
our $menu = [		
		'Update Ohlone Classes from Datatel List',
		'Update Instructors Emails from Datatel List',
		'Update Ohlone Degrees - from website',
		'Pull out emails from instructors who teach TBA/hybrid courses',
		'Update Programs Info'
	    ];
our @menu = @$menu;
@rubric = qw(0 1 2 3 4 5 6 7 8 9 10);
our @classes = ();
our %class_name = ();
#foreach (@classes) {
#    $class_name{$_} = $_;
#}
our @semester = ();
#our %semester_name = ();
#foreach (@semester) {
#    $semester_name{$_} = $_;
#}
our @year = qw(2009, 2010, 2011, 2012, 2013, 2014);
our %year_name = ();
foreach (@year) {
    $year_name{$_} = $_;
}
$area_fields = "id, title, description";
$SLO_fields = "ID, area, SLO, description";

@yes_no = qw(Yes No);

######################################################################
#### main begin here 			          ####################
######################################################################

#print ("am I even here with param? ", param, "\n<br />");
&print_header;

unless ( param ) {
   	print h1( "Assessment Tracker Organizer" );
	&print_options;
	&print_link;
}
else {
        #print "debug in the else: LAST: ", param('LAST'), "\n";

   	if ( param( "LAST" ) eq "MAIN" ) {
      		my $selection = param( "selection" );
                #print "debug: selection is $selection\n";
                
            	&input_datatel_class_sections( $dbh ) if ( $selection eq $menu[0] );
            	&input_datatel_instructor_emails( $dbh ) if ( $selection eq $menu[1] );
				&input_degrees( $dbh ) if ( $selection eq $menu[2] );
					#option below (TBA_Hybrid_emails) does not apply to this application
				&TBA_Hybrid_emails( $dbh ) if ( $selection eq $menu[3] );
				&input_programs_info( $dbh ) if ( $selection eq $menu[4] );
	}elsif ( param( "LAST" ) eq "PROCESS_CLASS_SECTIONS" ) {
                &process_class_sections( $dbh);
   	}elsif ( param( "LAST" ) eq "PROCESS_INSTRUCTOR_EMAILS" ) {
      		&process_instructor_emails( $dbh );
	}elsif ( param( "LAST" ) eq "PROCESS_DEGREES" ) {
      		&process_degrees( $dbh );
	}elsif ( param( "LAST" ) eq "PROCESS_TBA_SECTIONS" ) {
      		&process_TBA_Hybrid( $dbh );
	}elsif ( param( "LAST" ) eq "PROCESS_PROGRAMS_INFO" ) {
      		&process_programs_info( $dbh );
	}

	

   	$dbh->disconnect();
	&print_link;
}

print end_html();

###################################################################
#       input_datatel_class_sections
###################################################################
                
sub input_datatel_class_sections {
        print <<endHTML;
		<form action="organizer.cgi" method="post">
        <p><strong>Update Assessment Tracker with current list of courses
			from Datatel</strong> (to be done once per semester)
        <ol>
        <li>First step is to create a work order to IT with the following wording:
		<ul>
		 Please provide datatel info (as a .txt file) for all Ohlone course sections <br />
			in the following pipe delineated format and sorted by course symbol:<br />
			<ul>
			Course_symbol|Course_title<p>
			Example:<br />
			CS-101-01|Intro Computers and Info Tech<br />
			CS-101L-01|Computer Applicationn<br />
			CS-102-01|Intro to Programming Using C++<br />
			CS-102-02|Intro to Programming Using C++<br />
			</ul>
		</ul>

		
        <li>Once the list is received by email, select all the records, 
		 Copy, and 'Paste' in the text box below 
        <br />	<ul><textarea name="data" cols="80" rows="30"></textarea>
				</ul>
        <p>	<input type="submit" value="Submit" />
	<input type="hidden" name="LAST" value="PROCESS_CLASS_SECTIONS" />

		</ol>	

	
        </form>
endHTML
}     


######################################################################
# process_class_sections											##
# adds new classes to the 'classes' table if not alrady exists		##
######################################################################

sub process_class_sections
{
   	my($dbh) = (shift);
	my $new_data = param("data");	#pipe delineated text from datatel
	my @new_data = split(/\n/, $new_data);

	$new_data[-1] .= " ";	#add another character in the last record, since it is missing an extra return from the others.
	foreach my $new_data (@new_data) {
		chop $new_data;	#there is a ^M from the IT symbol 
			#split symbol, title
		my ($symbol, $new_title) = split(/\|/, $new_data);

			#get rid of section portion of class symbol and populate $department
			#example: CS-149-01, changed to CS-149 and $department = CS
		($d1, $d2, $d3) = split (/-/, $symbol);	#symbol looks like 'CS-149-01
		$new_department = $d1;
		$symbol = $d1 . "-" . $d2;

		$sql = "select ID from gen62_classes where symbol = '$symbol';";
			#print ("sql: $sql<br />");
		$sth = $dbh->prepare($sql);
			#print ("debug after 'prepare' statement<br />");
		$sth->execute();
			#print ("debug after execute statement<br />");
		my $row = $sth->fetchrow_hashref;
			#print ("debug with row: ", %$row, "\n<br />");
		my $old_id =  $row->{'ID'};

			#if match, just replace symbol address (whether changed or not) and udpdate 'validate' field 
		if ($old_id) {
				#print ("debug with about to use this command: " .
				#		"update classes set title = '$new_title', department= '$new_department' where id = '$old_id';");
			my $sql = "update gen62_classes set title = ?, program= '$new_department' where ID = '$old_id';";
			$sth = $dbh->prepare($sql );   
			$sth->execute($new_title) or die("table 'gen62_classes': ");
				#$sth = $dbh->prepare("update classes set title = '$new_title', department = '$new_department', 
				#		validate = ? where symbol = ?;");
				#$sth->execute($new_title, $new_department) or die("table 'SLO_rubrics': $DBI::errstr\n");
			print("Updated $symbol in table gen62_classes with $new_title and $new_department.\n<br />");
				#print("debug: ran this sql: $sql\n<br />");

			#else, add new class with 'validate' field
		}else {
				#print ("debug in the else (new record)<br />");
			$sql = "insert into gen62_classes values ('', '$symbol', ?, '$new_department', '', 'fall09');";
				#print ("debug with sql:$sql<br />");
				#$sth = $dbh->prepare("insert into classes values ('', ?, ?, ?);");
				#$sth->execute($symbol, $new_title, $new_department);
			$sth = $dbh->prepare($sql);
			$sth->execute($new_title);
			print("Added $new_title and $new_department with $symbol in table gen62_classes.\n<br />");
		}
	}
}

###################################################################
#       input_datatel_instructor_emails
###################################################################
                
sub input_datatel_instructor_emails {
        print <<endHTML;
        <form action="organizer.cgi" method="post">
        <p><strong>Update assessment program with current list of instructors
			from Datatel</strong> (to be done once per semester)
        <ol>
        <li>First step is to create a work order to IT with the following wording:
		<ul>
		 "Please provide datatel info (as a .txt file) for instructors and their emails<br />
			in the following pipe delineated format and sorted by last name:<br />
			<ul>
			Last_name|First_name|Email<p>
			Example:<br />
			Arellano|Rick|rarellano@ohlone.cc.ca.us<br />
			Degallier|Jon|jdegallier@ohlone.edu<br />
			Grotegut|Richard|rgrotegut@ohlone.edu"<br />
			</ul>
		</ul>

        <li>Once the list is received by email, select all the records, 
		 Copy, and 'Paste' in the text box below 
        <br />	<ul><textarea name="data" cols="80" rows="30"></textarea>
				</ul>
		<li>Enter semester and year (ex: SPRING 09): 
			<input type="text"  name="semester" />
        <p>	<input type="submit" value="Submit" />
		<input type="hidden" name="LAST" value="PROCESS_INSTRUCTOR_EMAILS" />
		</ol>
		</form>
endHTML
}     

######################################################################
#### process_instructor_emails		    			######
#### this routine updates instructors database			######
####								######
######################################################################

sub process_instructor_emails
{
    my($dbh) = (shift);
	my $new_data = param("data");	#pipe delineated text from datatel
	my @new_data = split(/\n/, $new_data);
	my $semester = param("semester");
	#print ("debug with instructor data: @new_data\n<p>");
	#print ("debug with semester: $semester\n<p>");

		#First, back up instructors db
		#open(OUT, ">../instructors_back_up") or die("could not open instructor_back_up for writing\n<br />");
	        #$sth = $dbh->prepare("select * from instructors;");
	        #$sth->execute() or die("table 'instructor': $DBI::errstr\n");
	        #while (my $row = $sth->fetchrow_hashref) {
		#	my $line_to_back_up = $row->{"first"} . "|" . $row->{"last"} . "|" . 
		#		$row->{"email"} . "|" . $row->{"validate"} .  "\n";
		#	print OUT $line_to_back_up;	
		#}
		#close OUT;
		#exit;

	foreach my $new_data (@new_data) {
        	chop $new_data;	#there is a ^M from the IT email 
			#split first, last, and email
			#use the following when restoring data from 'instructors_back_up'
			#my ($first, $last, $new_email) = split(/\|/, $new_data);	
		my ($last, $first, $new_email) = split(/\|/, $new_data);
			#chomp ($new_email);	#comment out when restoring data from 'instructors_back_up'
			#print ("last: $last and first: $first<br />");
			#search for first and last in database
	        	#$sth = $dbh->prepare("select email from instructors where first = ? and last = ?;");
	        	#$sth->execute( $first, $last) or die("table 'instructor': $DBI::errstr\n");
		$sql = "select id from instructors where first = '$first' and last = '$last';";
			#print ("sql: $sql<br />");
	        $sth = $dbh->prepare( $sql );
			#print ("debug after 'prepare' statement<br />");
	        $sth->execute();
			#print ("debug after execute statement<br />");
	        my $row = $sth->fetchrow_hashref;
	        	#print ("debug with row: ", %$row, "\n<br />");
	        my $old_id =  $row->{'id'};
			
		#if match, just replace email address (whether changed or not) and udpdate 'validate' field to semester data
		if ($old_id) {
			my $sql = "update instructors set semester = '$semester', email= '$new_email' where id = '$old_id';";		
		    	$sth = $dbh->prepare($sql); 
		    	$sth->execute() or die("table 'instructors': ");	
		        	#$sth = $dbh->prepare(" update instructors set email = '$new_email', 
				#		validate = ? where first = ? and last = ?;");

		        	#$sth->execute($semester, $first, $last) or die("table 'SLO_rubrics': $DBI::errstr\n");
			print("Updated $first and $last in table instructors with $new_email.\n<br />");
				#print("debug: ran this sql: $sql\n<br />");			
		#else, add new instructor with 'validate' field
		} else {
				#print ("debug in the else (new record)<br />");
			$sql = "insert into instructors values ('', '$new_email', '$first', '$last', '$semester');";
		        $sth = $dbh->prepare( $sql);
		        $sth->execute();
				#print ("debug with sql:$sql<br />");
				#$sth = $dbh->prepare("insert into instructors values ('', ?, ?, ?, ?);");
				#$sth->execute( $new_email, $first, $last, $semester);
			print("Added $first and $last with $new_email in table instructors.\n<br />");
		}		

	}
}

###################################################################
#       input_degrees
###################################################################
                
sub input_degrees {
        print <<endHTML;
                <form action="organizer.cgi" method="post">
        <p><strong>Update Assessment Tracker with current list of degrees/certificates
			from Ohlone website</strong> (to be done once per semester)
        <ol>
        <li>Copy the entire list from <a href="http://www.ohlone.edu/core/academicprograms.html">Ohlone Website</a>		
        <li>Paste-Special into spreadsheet by separtating the first column from the rest (use two spaces seperator)
		<ul>
		Example:
				<ul>
					A+ Certification Training|CNET<br /> 
					Animation and 3D Modeling (Multimedia)|MM<br /> 
					Anthropology: Cultural|ANTH <br />
					Anthropology: Physical|ANTH <br />
					etc.<br />
				</ul>
		</ul>
		<li>Copy the list of titles to paste below and submit.
			<br />
				<ul>
					<textarea name="data" cols="80" rows="30"></textarea>
				</ul>
			<p>	<input type="submit" value="Submit" />
				<input type="hidden" name="LAST" value="PROCESS_DEGREES" />
	  
		</ol>	

	
        </form>
endHTML
}     


######################################################################
#### process_degrees									##############
######################################################################

sub process_degrees
{
   	my($dbh) = (shift);
	my $new_data = param("data");	#pipe delineated text from datatel
	my @new_data = split(/\n/, $new_data);
	#print ("debug with classes data: @new_data\n<p>");

	$new_data[-1] .= " ";	#add another character in the last record, since it is missing an extra return from the others.
	foreach my $new_data (@new_data) {
		chop $new_data;	#there is a ^M from the IT symbol 
		#split symbol, title
        #my ($symbol, $new_department, $new_title) = split(/\|/, $new_data);	#use this when restoring data from 'instructors_back_up'
			$sql = "select id from degrees where title = ?;";
				#print ("sql: $sql<br />");
	        $sth = $dbh->prepare($sql);
				#print ("debug after 'prepare' statement<br />");
	        $sth->execute($new_data);
				#print ("debug after execute statement<br />");
	        my $row = $sth->fetchrow_hashref;
				#print ("debug with row: ", %$row, "\n<br />");
	        my $old_id =  $row->{'id'};

		#if match, just replace symbol address (whether changed or not) and udpdate 'validate' field 
		if ($old_id) {
				#print ("debug with about to use this command: " .
				#		"update classes set title = '$new_title', department= '$new_department' where id = '$old_id';");
			my $sql = "update degrees set title = ? where id = '$old_id';";
			$sth = $dbh->prepare($sql );   
			$sth->execute($new_data) or die("table 'classes': ");
					#$sth = $dbh->prepare("update classes set title = '$new_title', department = '$new_department', validate = ? where symbol = ?;");
					#$sth->execute($new_title, $new_department) or die("table 'SLO_rubrics': $DBI::errstr\n");
			print("Updated table degrees with $new_data.\n<br />");
					#print("debug: ran this sql: $sql\n<br />");

		#else, add new class with 'validate' field
		}
        else {
					#print ("debug in the else (new record)<br />");
				$sql = "insert into degrees values ('', ?);";
					#print ("debug with sql:$sql<br />");
					#$sth = $dbh->prepare("insert into classes values ('', ?, ?, ?);");
					#$sth->execute($symbol, $new_title, $new_department);
		        $sth = $dbh->prepare($sql);
		        $sth->execute($new_data);
				print("Added $new_data in table degrees.\n<br />");
		}
			
	}
}

###################################################################
#       TBA_Hybrid_emails
###################################################################
                
sub TBA_Hybrid_emails {
        print <<endHTML;
                <form action="organizer.cgi" method="post">
        <p><strong>More about DE than Assessment Tracker: Find instructors who teach TBA/Hybrid section<br />
			and return their emails</strong>
        <ol>
        <li>First step is to create a work order to IT with the following wording:
		<ul>
		 Please provide datatel info (as a .txt file) of all Ohlone course sections <br />
			and instructors teaching them in the following pipe delineated format and <br />
			sorted by course symbol:<br />
			<ul>
			Course_symbol|Course_title|first|last|email<p>
			Example:<br />
			AF-101B-01|Foundations of U.S. Air Force|Hellen|Bruce|bhellen@casa.sjsu.edu<br />
			AF-102B-01|Evolution USAF Air&Space Pwr|Hellen|Bruce|bhellen@casa.sjsu.edu<br />
			AH-110-01|Medical Terminology|Mangarova|Nedialka|Mangarova@hotmail.com<br />

			</ul>
		</ul>

		
        <li>Once the list is received by email, select all the records, 
		 Copy, and 'Paste' in the text box below 
        <br />	<ul><textarea name="data1" cols="80" rows="30"></textarea>
				</ul>
        <li>next step is to copy and paste a list of courses, which are being converted from TBA<br />
				to Hybrid in this format in the text area below:
			<ul>
			Course_symbol|Course_title<p>
			Example:<br />
			BRDC-134|Final Cut Pro Editing<br />
			BRDC-135|Final Cut Pro-Adv Techniques<br />
			BRDC-136|Digital Video and Lighting<br />

			</ul>
		</ul>
        <br />	<ul><textarea name="data2" cols="80" rows="30"></textarea>
				</ul>

        <p>	<input type="submit" value="Submit" />
	<input type="hidden" name="LAST" value="PROCESS_TBA_SECTIONS" />

		</ol>	

	
        </form>
endHTML
}     


######################################################################
#### process_TBA_Hybrid									##############
######################################################################

sub process_TBA_Hybrid
{
   	my($dbh) = (shift);
	my $new_data1 = param("data1");	#pipe delineated text from datatel
	my @new_data1 = split(/\n/, $new_data1);
		#print ("debug with classes data: @new_data1\n<p>");
	my $new_data2 = param("data2");	#pipe delineated text from TBA list
	my @new_data2 = split(/\n/, $new_data2);
		#print ("debug with TBA class data: @new_data2\n<p>");
	$new_data1[-1] .= " ";	#add another character in the last record, since it is missing an extra return from the others.
	$new_data2[-1] .= " ";	#add another character in the last record, since it is missing an extra return from the others.
	my $email_list = "";	#final list of emails, separated by commas
	my @email_array = ();	#first put in array with duplicates
	my %email_hash = ();	#next put into hash to get rid of duplicates
	
	foreach my $new_data2 (@new_data2) {			#loop from the TBA list of classes
		chop $new_data2;	#there is a ^M from the IT symbol 
		#split symbol, title
        #my ($symbol, $new_department, $new_title) = split(/\|/, $new_data);	#use this when restoring data from 'instructors_back_up'
		my ($symbol2, $d1) = split(/\|/, $new_data2);
		foreach my $new_data1 (@new_data1) {		#loop list of all classes for a semester for match in TBA list
			my $temp = $new_data1;
			chop $temp;	#there is a ^M from the IT symbol 
				#split symbol, title
				#my ($symbol, $new_department, $new_title) = split(/\|/, $new_data);	#use this when restoring data from 'instructors_back_up'
			my ($symbol1, $title, $first, $last, $email) = split(/\|/, $temp);
	
				#get rid of section portion of class symbol and populate $department
				#example: CS-149-01, changed to CS-149 and $department = CS
			($d1, $d2, $d3) = split (/-/, $symbol1);	#symbol looks like 'CS-149-01
				#$new_department = $d1;
			$symbol1 = $d1 . "-" . $d2;
			if ($symbol2 eq $symbol1) {
				push (@email_array, $email);
					#print ("debug with $symbol1 with $email<br>\n");
			}
		}
	}
		#print ("debug with email_array: @email_array<br>");
		#then clean up duplicate emails
	foreach (@email_array) {
		if ( exists($email_hash{$_} )) {
			#print ("$_ is duplicated<br>");
		}else {
			$email_hash{$_} = $_;
		}
	}
	foreach (keys %email_hash) {
		$email_list .= $_ . ",";
		print ("$_<br>");
	}
	print <<endHTML;
	<h3>List of all instructors teaching a course to be converted from TBA to Hybrid, <br />
			either in the fall09 or spring10<p />
	</h3>
	Copy and paste these addresses in your email :)<p />
endHTML
	print ("$email_list<br>\n");
	
}

###################################################################
#   input_programs_info (not complete - just pasted from input_datatel_class_sections
#		with wording changed for list request below)
###################################################################
                
sub input_programs_info {
        print <<endHTML;
                <form action="organizer.cgi" method="post">
        <p><strong>Update Assessment Tracker with current list of programs</strong>
		<ol>
        <li>Provide a list in the following format <br />
			<ul>
			TOP code|abbreviation|full name|type<p>
			Example:<br />
			07000|CS|Computer Science|I<br />
			04000|BIO|Biology|I<br />
			62000||Admissions & Records|AS
			</ul>
			Note that programs, which are not of type 'I' do have abbreviations and the 
				second field is left empty (Admissions & Records)<p />
		
        <li>Once the list is received by email, select all the records, 
		 Copy, and 'Paste' in the text box below 
        <br />	<ul><textarea name="data" cols="80" rows="30"></textarea>
				</ul>
        <p>	<input type="submit" value="Submit" />
	<input type="hidden" name="LAST" value="PROCESS_PROGRAMS_INFO" />

		</ol>	

	
        </form>
endHTML
}     

######################################################################
#### process_programs_info	(not complete - just pasted from process_class_sections)
######################################################################

sub process_programs_info
{
   	my($dbh) = (shift);
	my $new_data = param("data");	#pipe delineated text from datatel
	my @new_data = split(/\n/, $new_data);
	#print ("debug with classes data: @new_data\n<p>");


		#First, back up classes db
		#open(OUT, ">../classes_back_up") or die("could not open classes_back_up for writing\n<br />");
	        #$sth = $dbh->prepare("select * from classes;");
	        #$sth->execute() or die("table 'classes': $DBI::errstr\n");
	        #while (my $row = $sth->fetchrow_hashref) {
		#	my $line_to_back_up = $row->{"department"} . "|" . $row->{"last"} . "|" . 
		#		$row->{"symbol"} . "|" . $row->{"validate"} .  "\n";
		#	print OUT $line_to_back_up;	
		#}
		#close OUT;
		#exit;
	$new_data[-1] .= " ";	#add another character in the last record, since it is missing an extra return from the others.
	foreach my $new_data (@new_data) {
		chop $new_data;	#there is a ^M from the IT symbol 
		#split symbol, title
        #my ($symbol, $new_department, $new_title) = split(/\|/, $new_data);	#use this when restoring data from 'instructors_back_up'
		my ($code, $abbreviation, $full_name, $type) = split(/\|/, $new_data);

		#get rid of section portion of class symbol and populate $department
			#example: CS-149-01, changed to CS-149 and $department = CS

		#print ("debug with new symbol: $symbol and department: $department<br>");


		#chomp ($new_department);	#comment out when restoring data from 'classes_back_up'
		#print ("title: $new_title and department: $new_department<br />");

		#search for department and title in database
				#$sth = $dbh->prepare("select id from classes where symbol = ?;");
				#$sth->execute($symbol) or die("table 'classes': $DBI::errstr\n");
			$sql = "select id from gen62_programs where code = '$code';";
				#print ("sql: $sql<br />");
	        $sth = $dbh->prepare($sql);
				#print ("debug after 'prepare' statement<br />");
	        $sth->execute();
				#print ("debug after execute statement<br />");
	        my $row = $sth->fetchrow_hashref;
				#print ("debug with row: ", %$row, "\n<br />");
	        my $old_id =  $row->{'id'};

		#if match, just replace symbol address (whether changed or not) and udpdate 'validate' field 
		if ($old_id) {
				#print ("debug with about to use this command: " .
				#		"update classes set title = '$new_title', department= '$new_department' where id = '$old_id';");
			my $sql = "update gen62_programs set code = ?, 
						abbreviation = '$abbreviation', full_name = '$full_name', type = '$type'
						where id = '$old_id';";
			$sth = $dbh->prepare($sql );   
			$sth->execute($code) or die("table 'gen62_programs': ");
					#$sth = $dbh->prepare("update classes set title = '$new_title', department = '$new_department', validate = ? where symbol = ?;");
					#$sth->execute($new_title, $new_department) or die("table 'SLO_rubrics': $DBI::errstr\n");
			print("Updated $code in table gen62_programs to include $full_name and $abbreviation and $type.\n<br />");
					#print("debug: ran this sql: $sql\n<br />");

		#else, add new class with 'validate' field
		}
        else {
					#print ("debug in the else (new record)<br />");
				$sql = "insert into gen62_programs values ('', '$code', '$abbreviation', ?, '$type');";
					#print ("debug with sql:$sql<br />");
					#$sth = $dbh->prepare("insert into classes values ('', ?, ?, ?);");
					#$sth->execute($symbol, $new_title, $new_department);
		        $sth = $dbh->prepare($sql);
		        $sth->execute($full_name);
				print("Added $full_name ... $abbreviation code $code type $type in table gen62_programs.\n<br />");
		}
			
	}
}


######################################################################
#### open_file						    ##########
######################################################################
sub open_file {
	my $file_name = shift;
	open(IN, "$file_name") or die("won't open all_classes_datatel.txt\b<br />");
	my @file = <IN>;
	close IN;
	return @file;
}

                
################################################################
###			print_header 					####
################################################################

sub print_header {
	#print header();
	print <<end; 
   	<head> <title>Classes Organizer </title>
	<style type="text/css">
	<!--
	body {font-family: arial, helvetica, sans serif; color: #330066; background-color: white;}
	a {text-decoration:none; cursor:hand; }
	a:link {color: #0000FF; text-decoration: underline; }
	a:visited {color: #660000; text-decoration: underline;}
	a:active {color: #ff0000; text-decoration: none;}
	a:hover {color: #666666; text-decoration: none;}
	-->
	</style>
	</head>
	<body>
	    <table align=center width="600" border="0" cellspacing="0" cellpadding="0">
    <tr>
        <td align="center"><a href="http://www.ohlone.edu/index.html">
            <img src="http://www.fremont.k12.ca.us/cms/lib04/CA01000848/Centricity/Domain/3100/Ohlone_College_logo.jpg" width=150 height=75
                 border=0 alt="ohlone.edu"></a></td><br>    </tr>
    <tr>
        <td align="center"><h3>Online Assessment Tracker - Update Classes Database Info</h3>
		<font color="green">Thanks to Joy Hughes and Perl Class of Spring 09</font><p> 
	</tr>
    </table>
end
}

######################################################################
#### print_options					       #######
######################################################################


sub print_options {
	print 
         start_form(),
         popup_menu( -name => 'selection',
                     -value => $menu ),
         hidden( { -name => "LAST", -value => "MAIN" } ),
         br(), br(), br(), br(), br(),
         submit( -value => "Click to Proceed" ),
         end_form();
}

######################################################################
#### print_link 					       #######
######################################################################

sub print_link {
	print	p(),
                a( { -href => "organizer.cgi" }, 
         		"Back to the Assessment Project Database Options" ),

}


######################################################################
#### generic query to pull data from the database           ##########
######################################################################
        
sub getRecords{
        my ($dbh, $mySQLString) =  @_;
   	#print("<p>Here in getRecords value of SQL string is $mySQLString</p>\n");
       
        my $sth = $dbh->prepare($mySQLString);
   	$sth->execute();
                  
   	my $rows = $sth->fetchall_arrayref();
   	#print("debug:<p>Here in getRecords value of full_row array is: @{$rows}</p>\n");
        $sth->finish();
   	return $rows;
} # end getRecords
        
