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
