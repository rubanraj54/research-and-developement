# research-and-developement
Docker files and program files to evaluate performance for different database

For more information about how to run programs, visit github repository.

https://github.com/rubanraj54/research-and-developement

This research work is divided in to two main sections,

* Qualitative analysis
* Quantitative analysis

Below table shows the quick summary of Qualitative comparison of different databases. Analysis has been done based on database architecture and other features such as data model, consistency, availability, partition tolerance, query language, language support, schema, storage options, distributed architecture, immutable data and license type.

![Preview](https://raw.githubusercontent.com/rubanraj54/research-and-developement/master/images/g10997.png)

General schema used for all database.

#### Location Event
<pre>
{
	'robot_id' : _robot_id #integer 24bytes
	'latitude' : random.uniform(1.0, 100.0), #float 24bytes
	'longitude' : random.uniform(1.0, 100.0), #float 24bytes
	'offset' : random.uniform(1.0, 100.0), #float 24bytes
	'accuracy' : random.uniform(1.0, 100.0), #float 24bytes
	'timestamp' : datetime.datetime.now() #datetime 48bytes
}
</pre>

#### Ultrasonic Sensor Event
<pre>
{
	'robot_id' : _robot_id #integer 24bytes
	'voltage' : random.uniform(1.0, 100.0), #float 24bytes
	'timestamp' : datetime.datetime.now() #datetime 48bytes
}
</pre>

#### MotorVoltage Event
<pre>
{
	'robot_id' : _robot_id #integer 24bytes
	'motor_id' : random.randint(1, 10), #float 24bytes
	'voltage' : random.uniform(1.0, 100.0), #float 24bytes
	'current' : random.uniform(1.0, 100.0), #float 24bytes
	'timestamp' : datetime.datetime.now() #datetime 48bytes
}
</pre>

#### Pose Event
<pre>
{
	'robot_id' : _robot_id #integer 24bytes
	'x' : random.uniform(1.0, 100.0), #float 24bytes
	'y' : random.uniform(1.0, 100.0), #float 24bytes
	'z' : random.uniform(1.0, 100.0), #float 24bytes
	'theta' : random.uniform(1.0, 100.0), #float 24bytes
	'timestamp' : datetime.datetime.now() #datetime 48bytes
}
</pre>

#### RGB Event (Without blob)
<pre>
{
	'robot_id' : _robot_id #integer 24bytes
	'image_base64': big_image_base64_path, #string >60bytes
	'blob' : False, #boolean 24bytes
	'timestamp' : datetime.datetime.now() #datetime 48bytes
}
</pre>

#### RGB Event (With blob)
<pre>
{
	'robot_id' : _robot_id #integer 24bytes
	'image_base64': big_image_base64, #string (Buffer) > 1 Mega byte
	'blob' : False, #boolean 24 bytes
	'timestamp' : datetime.datetime.now() #datetime 48 bytes
}
</pre>

Note : For individual database schema, please check corresponding folders.
