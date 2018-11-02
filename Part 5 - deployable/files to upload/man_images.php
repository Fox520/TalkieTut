<?php

$uploaddir = 'img/';
if(isset($_FILES['testname']['name'])){
	$uploadfile = $uploaddir . basename($_FILES['testname']['name']);

	if(move_uploaded_file($_FILES['testname']['tmp_name'], $uploadfile)){
		echo "Uploaded";
	}
}else{
    echo "Not uploaded";
}

?>