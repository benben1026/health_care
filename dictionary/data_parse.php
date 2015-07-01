<?php
	ini_set('display_errors',1);
	ini_set('display_startup_errors',1);
	error_reporting(-1);

	function search_symptom($stmt_search_symptom, $symptom){
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

	$host = "localhost";
	$username = "healthcare";
	$password = "hvVZVuRbSZjdREZ6";
	$database = "healthcare";

	$filename_prefix = "data/disease_";

	$link = new mysqli($host, $username, $password, $database);
	if($link->connect_error){
		echo "Failed to connect to MySQL: (" . $link->connect_errno . ") " . $link->connect_error . "\n";
	}
	echo "Connect to Database successfully\n";
	$stmt_insert_disease = $link->prepare("INSERT INTO Disease(disease_name) VALUES(?)");
	//echo var_dump($stmt_insert_disease);
	$stmt_update_attribute = $link->prepare("UPDATE Disease SET treatment=?, causes=?, prevention=?, description=? WHERE disease_id=?");
	//echo var_dump($stmt_update_attribute);
	$stmt_insert_symptom = $link->prepare("INSERT INTO Symptom(symptom_name) VALUES(?)");
	//echo var_dump($stmt_insert_symptom);
	$stmt_search_symptom = $link->prepare("SELECT symptom_id FROM Symptom WHERE symptom_name = ?");
	//echo var_dump($stmt_search_symptom);
	$stmt_insert_relationship = $link->prepare("INSERT INTO Disease_Has_Symptom(disease_id, symptom_id) VALUES(?, ?)");

	for($index = "A"; ord($index) <= ord("Z"); $index =chr(ord($index) + 1)){
		$file = fopen($filename_prefix . $index, "r");
		$content_raw = fread($file, filesize($filename_prefix . $index));
		$content = json_decode($content_raw);
		fclose($file);

		foreach($content as $disease_name => $disease){
			$stmt_insert_disease->bind_param("s", $disease_name);
			if(!$stmt_insert_disease->execute()){
				echo "Fail to insert disease " . $disease_name . ":" . $stmt_insert_disease->error . "\n";
				break;
			}
			echo "Disease Inserted: " . $disease_name . "\n";
			$disease_id = $link->insert_id;
			$attribute_list["treatment"] = "";
			$attribute_list["causes"] = "";
			$attribute_list["prevention"] = "";
			$attribute_list["description"] = "";

			foreach($disease as $attribute_name => $attribute){
				if(strtolower($attribute_name) == "symptoms"){
					foreach($attribute as $symptom){
						//$symptom_table = get_symptom_table();
						//$symptom_id = binary_search_symptom($symptom, $symptom_table, 0, sizeof($symptom_table) - 1);
						$symptom_id = search_symptom($stmt_search_symptom, $symptom);
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
					continue;
				}
				if(strtolower($attribute_name) != "treatment" && strtolower($attribute_name) != "causes" && strtolower($attribute_name) != "prevention" && strtolower($attribute_name) != "description"){
					echo "No such attribute:" . $attribute_name . "\n";
					continue;
				}
				$attribute_list[strtolower($attribute_name)] = $attribute;
			}
			echo "treatment:" . $attribute_list["treatment"] . "\n";
			echo "causes:" . $attribute_list["causes"] . "\n";
			echo "prevention:" . $attribute_list["prevention"] . "\n";
			echo "description:" . $attribute_list["description"] . "\n";
			$stmt_update_attribute->bind_param("ssssi", $attribute_list["treatment"], $attribute_list["causes"], $attribute_list["prevention"], $attribute_list["description"], $disease_id);
			if(!$stmt_update_attribute->execute()){
				echo "Fail to update attribute:" . $stmt_update_attribute->error . "\n";
			}
		}
		echo $index . " done!" . "\n";
	}

	mysqli_stmt_close($stmt_insert_disease);
	mysqli_stmt_close($stmt_update_attribute);
	mysqli_stmt_close($stmt_insert_symptom);
	mysqli_stmt_close($stmt_search_symptom);
	mysqli_stmt_close($stmt_insert_relationship);
	mysqli_close($link);



	/*
	function binary_search_symptom($symptom, $symptom_table, $left, $right){
		if($left < $right)
			return -1;

		$mid = round(($right + $left) / 2);
		if($symptom_table[$mid] == $symptom)
			return $mid;
		else if($symptom_table[$mid] < $symptom)
			return binary_search_symptom($symptom, $symptom_table, $left, $mid - 1);
		else
			return binary_search_symptom($symptom, $symptom_table, $mid + 1, $right);
	}

	function get_symptom_table(){
		$query = "SELECT * FROM `disease`";
		$result = mysqli_query($link, $query);
		for($i = 0; $row = mysqli_fetch_assoc($result); $i++){
			$symptom_table[$i] = $row;
		}
		return $symptom_table;
	}
	*/
?>