public fun TRCH__add(in _path, out _nidout)
{
    write(*, _path);
    DevAddStart(_path, 'TRCH', 49, _nidout);

    DevAddNode(_path // ':NAME', 'TEXT', *, *, _nid);
    DevAddNode(_path // ':COMMENT', 'TEXT', *, *, _nid);
    DevAddNode(_path // ':CHANNELS', 'NUMERIC', 6, *, _nid);
    DevAddNode(_path // ':CHAN_OFFSET', 'NUMERIC', 0, *, _nid);
    DevAddNode(_path // ':CLOCK_MODE', 'TEXT', 'INTERNAL', *, _nid);
    DevAddNode(_path // ':TRIG_SOURCE', 'NUMERIC', 0, *, _nid);
    DevAddNode(_path // ':CLOCK_SOURCE', 'NUMERIC', *, *, _nid);
    DevAddNode(_path // ':FREQUENCY', 'NUMERIC', 1E4, *, _nid);
    DevAddNode(_path // ':USE_TIME', 'TEXT', 'TRUE', *, _nid);
    DevAddNode(_path // ':PTS', 'NUMERIC', *, *, _nid);

    for (_c = 1; _c <=6; _c++)
    {
        _cn = _path // '.CHANNEL_' // TEXT(_c, 1);
        DevAddNode(_cn, 'STRUCTURE', *, *, _nid);
    	DevAddNode(_cn // ':START_TIME', 'NUMERIC', 0., *, _nid);
        DevAddNode(_cn // ':END_TIME', 'NUMERIC', 1., *, _nid);
        DevAddNode(_cn // ':START_IDX', 'NUMERIC', *, *, _nid);
        DevAddNode(_cn // ':END_IDX', 'NUMERIC', *, *, _nid);
        DevAddNode(_cn // ':DATA', 'SIGNAL', *, '/compress_on_put/nomodel_write', _nid);
    }
    DevAddAction(_path//':INIT_ACTION', 'INIT', 'INIT', 50,'CAMAC_SERVER',getnci(_path, 'fullpath'), _nid);
    DevAddAction(_path//':STORE_ACTION', 'STORE','STORE', 50,'CAMAC_SERVER',getnci(_path, 'fullpath'), _nid);
    DevAddEnd();
}

/*public fun DevAddAction(in _actpath,in _phase,in _method,in _seq,in _server,in _devpath,out _nid)
{
  return(DevAddNode(_actpath,'ACTION',MAKE_ACTION(MAKE_DISPATCH(2,_server,_phase,_seq,*),
             MAKE_METHOD(*,_method,BUILD_PATH(_devpath))),'/noshot_write',_nid));
}*/

