from pytz import timezone
import datetime, json, pytz


# print(timezone)
# mst = timezone('MST')

# appt_time_mst = datetime.datetime.now(mst)
# print("MST", appt_time_mst)

# now_time_mst = ((str(appt_time_mst)).split("."))[0]
# print(now_time_mst)

# now_time_mst_strptime = datetime.datetime.strptime(now_time_mst, "%Y-%m-%d %H:%M:%S")
# print(now_time_mst_strptime)

# mst_dt = mst.localize(now_time_mst_strptime, is_dst=None)
# utc_dt = mst_dt.astimezone(pytz.utc)
# print(utc_dt)


# utc = timezone('UTC')
# print("UTC", datetime.datetime.now(utc))



# d_str = "Mar 1st 2021 9:54 PM"
d_str = "Feb 11th 2021 9:03AM"
appt_time_obj = datetime.datetime.strptime(d_str, '%b %d %Y %I:%M%p')
print(appt_time_obj)

# datetime.datetime.strptime(appt_time_str, '%b %d %Y %I:%M%p')
# # print(d_str[:-1])
# if "th" in d_str:
#     d_str = d_str.replace("th", "")


# d_array = d_str.split(" ")
# d_timezone = d_array[len(d_array) - 1]
# print(d_timezone)

# d_time_str = ""
# for i in range(1, len(d_array) - 1):
#     if "am" in d_array[i].lower() or "pm" in d_array[i].lower():
#         d_time_str = d_time_str[:-1] + d_array[i]
#     else:
#         d_time_str = d_time_str + d_array[i] + " "

# print(d_time_str)        

# d_time_obj = datetime.datetime.strptime(d_time_str, '%b %d %Y %I:%M%p')
# print(d_time_obj)

# # appt_timezone = timezone(d_timezone)
# appt_timezone = timezone('US/Pacific')
# # appt_timezone = timezone('MST')

# print("Time in MST:", datetime.datetime.now(appt_timezone))
# # print(appt_timezone)

# appt_time = d_time_obj.astimezone(appt_timezone)

# print("timezone format", appt_time)

# appt_timestamp = datetime.datetime.timestamp(appt_time)
# print(appt_timestamp)






# d_str = "2021-02-11T09:00:00-07:00"
# print(d_str)
# d_obj = datetime.datetime.fromisoformat("2021-02-11T09:00:00-07:00")

# print(d_obj)