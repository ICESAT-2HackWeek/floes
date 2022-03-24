import icepyx as ipx

def get_files(path_root,short_name,datestr='None'):
    
    if short_name == "ATL07":
        pattern = "processed_"+short_name+"-02_{datetime:%Y%m%d%H%M%S}_{rgt:4}{cycle:2}{orbitsegment:2}_{version:3}_{revision:2}.h5"
    elif short_name == "ATL10":
        pattern = "processed_"+short_name+"-02_{datetime:%Y%m%d%H%M%S}_{rgt:4}{cycle:2}{orbitsegment:2}_{version:3}_{revision:2}.h5"
    else:
        pattern = "processed_"+short_name+"_{datetime:%Y%m%d%H%M%S}_{rgt:4}{cycle:2}{orbitsegment:2}_{version:3}_{revision:2}.h5"
        
    #pattern = "processed_ATL{product:2}_{datetime:%Y%m%d%H%M%S}_{rgt:4}{cycle:2}{orbitsegment:2}_{version:3}_{revision:2}.h5": SAMPLE
    
    print(path_root)
    reader = ipx.Read(path_root, short_name, pattern)

    file_list = reader._filelist
    
    return file_list

def see_available_files(short_name,spatial_extent,date_range,path_root,earthdata_uid=None):

    if earthdata_uid == 'hregan':
        email = 'heatherregan88@gmail.com'
    ## add other logins here
    
    region_a = ipx.Query(short_name, spatial_extent, date_range)

    granule_list=region_a.avail_granules(ids=True)[0]
    
    return granule_list

def download_files(short_name,spatial_extent,date_range,path_root,earthdata_uid=None,tracks=None):

    if earthdata_uid == 'hregan':
        email = 'heatherregan88@gmail.com'
    ## add other logins here
    
    region_a = ipx.Query(short_name, spatial_extent, date_range)

    granule_list=region_a.avail_granules(ids=True)[0]
    
    if tracks is not None:
        print('proceeding')
        this_region = ipx.Query(short_name,spatial_extent, date_range, tracks=tracks)
        this_region.earthdata_login('hregan', 'heatherregan88@gmail.com')
        this_region.order_granules()
        this_region.download_granules(path_root)
    else:
        ## Load in carefully!
        ncnt = 1
        for ra in granule_list:
            proceed = 0
            rgt = ra[24:28] ## messy coding...

            print(rgt+', checked file '+str(ncnt)+' of '+str(len(granule_list)))
            
            this_region = ipx.Query(short_name,spatial_extent, date_range, tracks=rgt)
            this_region.earthdata_login('hregan', 'heatherregan88@gmail.com')
            this_region.order_granules()
            this_region.download_granules(path_root)
            ncnt = ncnt + 1
    
    return

def get_trackid(filename,short_name,path,remove_processed=1):
    
    ''' 
    This function is useful in determining what track we're looking at
    Useful for if we are checking we are using the same track from different ATLXX
    It is very hacky - advice on how to improve the hard-coding is welcome!
    '''
    start_val = len(path)
    if remove_processed:
        sv = start_val+24
    else:
        sv = start_val+34
    if short_name == "ATL07":
        trackid = filename[sv:sv+4]
    elif short_name == "ATL10":
        trackid = filename[sv:sv+4]
        
    return trackid