<?php
	ini_set('display_errors',1);
	ini_set('display_startup_errors',1);
	error_reporting(-1);

	//$filename = "NHS/testnhs";
	$filename = "NHS/NHS_DB.data";
	$host = "128.199.82.15";
	$username = "healthcare";
	$password = "sf4e5UcjjFhy8u2z";
	$database = "healthcare";

	$link = new mysqli($host, $username, $password, $database);
	if($link->connect_error){
		echo "Failed to connect to MySQL: (" . $link->connect_errno . ") " . $link->connect_error . "\n";
		exit();
	}
	$stmt_insert_disease = $link->prepare("INSERT INTO Disease(disease_name) VALUES(?)");
	$stmt_update_attribute = $link->prepare("UPDATE Disease SET treatment=?, causes=?, prevention=?, description=?, `possible complications`=?, `exams and tests`=?, `gender`=? WHERE disease_id=?");
	$stmt_insert_symptom = $link->prepare("INSERT INTO Symptom(symptom_name) VALUES(?)");
	$stmt_search_symptom = $link->prepare("SELECT symptom_id FROM Symptom WHERE symptom_name = ?");
	$stmt_insert_relationship = $link->prepare("INSERT INTO Disease_Has_Symptom(disease_id, symptom_id) VALUES(?, ?)");
	
	process_data();	

	function process_data(){
		global $filename, $link;
		global $stmt_insert_disease, $stmt_update_attribute, $stmt_insert_symptom, $stmt_search_symptom, $stmt_insert_relationship;
		$file = fopen($filename, "r");
		$content = json_decode(fread($file, filesize($filename)));
		fclose($file);
		echo "Total Disease = " . count($content) . "\n";
		$i = 0;
		foreach($content as $name => $disease){
			$stmt_insert_disease->bind_param("s", $name);
			if(!$stmt_insert_disease->execute()){
				echo "Fail to insert " . $name . ":" . $stmt_insert_disease->error . "\n";
				continue;
			}
			insert_attr($disease, $link->insert_id);
			$i++;
			if($i % 100 == 0){
				echo $i / 100 * count($content) . "% ";
			}
		}
		mysqli_stmt_close($stmt_insert_disease);
		mysqli_stmt_close($stmt_update_attribute);
		mysqli_stmt_close($stmt_insert_symptom);
		mysqli_stmt_close($stmt_search_symptom);
		mysqli_stmt_close($stmt_insert_relationship);
		mysqli_close($link);
	}

	function insert_attr($data, $disease_id){
		global $stmt_update_attribute;
		$attribute_list["treatment"] = "";
		$attribute_list["causes"] = "";
		$attribute_list["prevention"] = "";
		$attribute_list["description"] = "";
		$attribute_list["possible complications"] = "";
		$attribute_list["exams and tests"] = "";
		$gender = "both"; //ENUM(male, female, both)
		foreach($data as $key => $value){
			if(strrpos(strtolower($key), "symptom") > -1){
				//echo "enter symptom";
				insert_symptom($value, $disease_id);
			}else if(strrpos(strtolower($key), "gender") > -1){
				if(!isset($value->Male))
					$gender = "female";
				if(!isset($value->Female))
					$gender = "male";
			}else if(strrpos(strtolower($key), "position") > -1 && isset($value->level1) && isset($value->level2)){
				//echo "value = " . $value[""];
				//echo "level 1 = " . $value["level1"] . "; level 2 = " . $value["level2"] . "\n";
				insert_position($disease_id, $value->level1, $value->level2);
			}else if(strrpos(strtolower($key), "introduction") > -1){
				$attribute_list["description"] = concatenate_attr($value);
			}else if(strrpos(strtolower($key), "complication") > -1){
				$attribute_list["possible complications"] = concatenate_attr($value);
			}else if(strrpos(strtolower($key), "treatment") > -1){
				$attribute_list["treatment"] = concatenate_attr($value);
			}else if(strrpos(strtolower($key), "diagnosis") > -1){
				$attribute_list["exams and tests"] = concatenate_attr($value);
			}else if(strrpos(strtolower($key), "cause") > -1){
				$attribute_list["causes"] = concatenate_attr($value);
			}
		}

		$stmt_update_attribute->bind_param("sssssssi", $attribute_list["treatment"], $attribute_list["causes"], $attribute_list["prevention"], $attribute_list["description"], $attribute_list["possible complications"], $attribute_list["exams and tests"], $gender, $disease_id);
		if(!$stmt_update_attribute->execute()){
			echo "Fail to update attribute:" . $stmt_update_attribute->error . "\n";
		}
	}

	function concatenate_attr($attr){
		$str = "";
		foreach($attr as $key => $value){
			$str .= "#%#" . $key . "#%#" . $value;
		}
		return $str;
	}

	function insert_symptom($symptoms, $disease_id){
		global $link;
		global $stmt_insert_disease, $stmt_update_attribute, $stmt_insert_symptom, $stmt_search_symptom, $stmt_insert_relationship;
		
		foreach($symptoms as $symptom){
			$symptom_id = search_symptom($symptom);
			if($symptom_id == -1){
				$stmt_insert_symptom->bind_param("s", $symptom);
				if(!$stmt_insert_symptom->execute()){
					echo "Fail to insert symptom " . $symptom . ": " . $stmt_insert_symptom->error ."\n";
					continue;
				}
				$symptom_id = $link->insert_id;
			}
			$stmt_insert_relationship->bind_param("ii", $disease_id, $symptom_id);
			if(!$stmt_insert_relationship->execute()){
				echo "Fail to update Disease_Has_Symptom table:" . $stmt_insert_relationship->error . "\n";
			}
		}
	}

	function search_symptom($symptom){
		global $stmt_insert_disease, $stmt_update_attribute, $stmt_insert_symptom, $stmt_search_symptom, $stmt_insert_relationship;
		
		$stmt_search_symptom->bind_param("s", $symptom);
		$stmt_search_symptom->execute();
		$stmt_search_symptom->bind_result($symptom_id);
		$stmt_search_symptom->store_result();
		if($stmt_search_symptom->fetch()){
			return $symptom_id;
		}else{
			return -1;
		}
	}

	function insert_position($disease_id, $position1, $position2){
		global $link;

		$stmt_search_position1 = $link->prepare("SELECT id FROM Body_Level1 WHERE name=?");
		$stmt_search_position2 = $link->prepare("SELECT id FROM Body_Level2 WHERE id=? AND name=?");
		$stmt_insert_position1 = $link->prepare("INSERT INTO Body_Level1(`name`) VALUES(?)");
		$stmt_insert_position2 = $link->prepare("INSERT INTO Body_Level2(`name`, `upper_level_id`) VALUES(?, ?)");


		$stmt_search_position1->bind_param("s", $position1);
		$stmt_search_position1->execute();
		$stmt_search_position1->bind_result($position1_id);
		$stmt_search_position1->store_result();
		if($stmt_search_position1->fetch()){
			//position 1 found
			$stmt_search_position2->bind_param("is", $position1_id, $position2);
			$stmt_search_position2->execute();
			$stmt_search_position2->bind_result($position2_id);
			$stmt_search_position2->store_result();
			if(!$stmt_search_position2->fetch()){
				//position 2 not found
				$stmt_insert_position2->bind_param("si", $position2, $position1_id);
				if(!$stmt_insert_position2->execute()){
					echo "Fail to add position2(1): " . $position2 . " Error:" . $stmt_insert_position2->error . "\n";
					return false;
				}else{
					$position2_id = $link->insert_id;
				}
			}
		}else{
			//position 1 not found
			$stmt_insert_position1->bind_param("s", $position1);
			if($stmt_insert_position1->execute()){
				$position1_id = $link->insert_id;
				$stmt_insert_position2->bind_param("si", $position2, $position1_id);
				if($stmt_insert_position2->execute()){
					$position2_id = $link->insert_id;
				}else{
					echo "Fail to add position2(2): " . $position2 . " Error:" . $stmt_insert_position2->error . "\n";
					return false;
				}
			}else{
				echo "Fail to add position1: " . $position1 . " Error:" . $stmt_insert_position1->error . "\n";
				return false;
			}
		}

		$stmt_insert_position = $link->prepare("UPDATE Disease SET body_part_1=?, body_part_2=? WHERE disease_id=?");
		$stmt_insert_position->bind_param("iii", $position1_id, $position2_id, $disease_id);
		if(!$stmt_insert_position->execute()){
			echo "Fail to add position into disease table: " . $disease_id . " Error:" . $stmt_insert_position1->error . "\n";
			return false;
		}
		mysqli_stmt_close($stmt_search_position1);
		mysqli_stmt_close($stmt_search_position2);
		mysqli_stmt_close($stmt_insert_position1);
		mysqli_stmt_close($stmt_insert_position2);
		mysqli_stmt_close($stmt_insert_position);
		return true;
	}

?>