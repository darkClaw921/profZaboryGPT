<?php
$user = '068578';
$from = date('d.m.Y');
$to = date('d.m.Y');
$type = '0';
$state = '0';
$tree = '';
$showTreeId = '1';
$fromNumber = '';
$numbersRinged = 0;
$numbersInvolved = 0;
$names = 0;
$outgoingLine = 1;
$toNumber = '';
$toAnswer = '';
$anonymous = '1';
$firstTime = '0';
$dtmfUserAnswer = 0;
$secret = '0.dj578vc0ce';

$hashString = join('+', array($anonymous, $dtmfUserAnswer, $firstTime, $from, $fromNumber, $names, $numbersInvolved, $numbersRinged, $outgoingLine, $showTreeId, $state, $to, $toAnswer, $toNumber, $tree, $type, $user, $secret));
$hash = md5($hashString);

$url = 'https://sipuni.com/api/statistic/export';
$query = http_build_query(array(
    'anonymous' => $anonymous,
    'firstTime' => $firstTime,
    'from' => $from,
    'fromNumber' => $fromNumber,
    'numbersRinged' => $numbersRinged,
    'outgoingLine' => $outgoingLine,
    'showTreeId' => $showTreeId,
    'state' => $state,
    'to' => $to,
    'toAnswer' => $toAnswer,
    'toNumber' => $toNumber,
    'tree' => $tree,
    'type' => $type,
    'user' => $user,
    'dtmfUserAnswer' => $dtmfUserAnswer,
    'hash' => $hash,
));

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $query);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$output = curl_exec($ch);
curl_close($ch);

header("Content-Disposition: attachment; filename=stat_$from-$to.csv");
echo $output;