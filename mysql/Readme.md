Schema representation for the following tables which was used for quantitative analysis.

Tables used to store sensor data are,
<pre>
+---------------------------+  
| handle_bar_voltage_events |  
| location_events           |  
| motor_voltage_events      |  
| pose_events               |  
| rgb_events                |  
+---------------------------+  
</pre>

### "handle_bar_voltage_events" table schema

<pre>
+-----------+---------+------+-----+---------+-------+
| Field     | Type    | Null | Key | Default | Extra |
+-----------+---------+------+-----+---------+-------+
| robot_id  | int(11) | YES  |     | NULL    |       |
| voltage   | float   | YES  |     | NULL    |       |
| timestamp | int(11) | YES  |     | NULL    |       |
+-----------+---------+------+-----+---------+-------+ 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
</pre>


### "location_events" table schema

<pre>
+-----------+---------+------+-----+---------+-------+
| Field     | Type    | Null | Key | Default | Extra |
+-----------+---------+------+-----+---------+-------+
| robot_id  | int(11) | YES  |     | NULL    |       |
| latitude  | float   | YES  |     | NULL    |       |
| longitude | float   | YES  |     | NULL    |       |
| offset    | float   | YES  |     | NULL    |       |
| timestamp | int(11) | YES  |     | NULL    |       |
| accuracy  | float   | YES  |     | NULL    |       |
+-----------+---------+------+-----+---------+-------+
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
</pre>


### "motor_voltage_events" table schema

<pre>
+-----------+---------+------+-----+---------+-------+
| Field     | Type    | Null | Key | Default | Extra |
+-----------+---------+------+-----+---------+-------+
| robot_id  | int(11) | YES  |     | NULL    |       |
| voltage   | float   | YES  |     | NULL    |       |
| current   | float   | YES  |     | NULL    |       |
| timestamp | int(11) | YES  |     | NULL    |       |
+-----------+---------+------+-----+---------+-------+
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
</pre>


### "pose_events" table schema

<pre>
+-----------+---------+------+-----+---------+-------+
| Field     | Type    | Null | Key | Default | Extra |
+-----------+---------+------+-----+---------+-------+
| robot_id  | int(11) | YES  |     | NULL    |       |
| x         | float   | YES  |     | NULL    |       |
| y         | float   | YES  |     | NULL    |       |
| z         | float   | YES  |     | NULL    |       |
| theta     | float   | YES  |     | NULL    |       |
| timestamp | int(11) | YES  |     | NULL    |       |
+-----------+---------+------+-----+---------+-------+
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
</pre>


### "rgb_events" table schema

<pre>
+--------------+------------+------+-----+---------+-------+
| Field        | Type       | Null | Key | Default | Extra |
+--------------+------------+------+-----+---------+-------+
| robot_id     | int(11)    | YES  |     | NULL    |       |
| image_base64 | longtext   | YES  |     | NULL    |       |
| blobflag     | tinyint(4) | YES  |     | NULL    |       |
| timestamp    | int(11)    | YES  |     | NULL    |       |
+--------------+------------+------+-----+---------+-------+
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
</pre>

One can adapt the mysql workbench for their own events/sensor data by following below steps,
* Create a new table to store data from new event.
* To create a new table, execute following command in mysql terminal.
* create table `table_name` (parameters...); 
* For eg. create table `location_events` (robot_id int,latitude float,longitude float,offset float,timestamp int,accuracy float);
* Once successfully created new table, go to mysql/src/utils.py file and add new event information in `create_event()`, `get_event()`, and `run_read_query()`.

#### How to run write scenario for existing scenario:
<pre>
python replication_test_write.py param_one param_two param_three param_four  
param_one = robot_id (integer)
param_two = frequency (integer in Hz)
param_three = minutes (integer)
param_four = usecase_name (string)
</pre>

#### How to run read scenario for existing scenario:
<pre>
python replication_test_read.py param_one param_two 
param_one = robot_id (integer)
param_two = usecase_name (string)
</pre>
