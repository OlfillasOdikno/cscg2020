    static SQFunctionProto *Create(SQSharedState *ss,SQInteger ninstructions,
        SQInteger nliterals,SQInteger nparameters,
        SQInteger nfunctions,SQInteger noutervalues,
        SQInteger nlineinfos,SQInteger nlocalvarinfos,SQInteger ndefaultparams)
    {
        SQFunctionProto *f;
        //I compact the whole class and members in a single memory allocation
        f = (SQFunctionProto *)sq_vm_malloc(_FUNC_SIZE(ninstructions,nliterals,nparameters,nfunctions,noutervalues,nlineinfos,nlocalvarinfos,ndefaultparams));
        new (f) SQFunctionProto(ss);
        f->_ninstructions = ninstructions;
        f->_literals = (SQObjectPtr*)&f->_instructions[ninstructions];
        f->_nliterals = nliterals;
        f->_parameters = (SQObjectPtr*)&f->_literals[nliterals];
        f->_nparameters = nparameters;
        f->_functions = (SQObjectPtr*)&f->_parameters[nparameters];
        f->_nfunctions = nfunctions;
        f->_outervalues = (SQOuterVar*)&f->_functions[nfunctions];
        f->_noutervalues = noutervalues;
        f->_lineinfos = (SQLineInfo *)&f->_outervalues[noutervalues];
        f->_nlineinfos = nlineinfos;
        f->_localvarinfos = (SQLocalVarInfo *)&f->_lineinfos[nlineinfos];
        f->_nlocalvarinfos = nlocalvarinfos;
        f->_defaultparams = (SQInteger *)&f->_localvarinfos[nlocalvarinfos];
        f->_ndefaultparams = ndefaultparams;
[...]