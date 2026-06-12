from typing import List
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.controller import OptimizationController
from app.models.enums.response import Response
from app.models.optimization.dto import *

# Create a new APIRouter instance for the optimizations
router = APIRouter()

# Create a new OptimizationController instance
controller: OptimizationController = OptimizationController()


@router.post('/optimizations',
             summary='Create and initialize an optimization for flights and target times.',
             status_code=status.HTTP_201_CREATED,
             response_model=OptimizationOutputBaseDTO,
             responses={
                 201: {'description': 'Optimization created successfully',
                       'content': {
                           'application/json': {
                               'example': {
                                   'optimization_id': 'UUID',
                                   'status': 'ENUM',
                               }
                           }
                       }},
             })
def post_optimization(optimization_input_dto: OptimizationInputDTO) -> JSONResponse | OptimizationOutputBaseDTO:
    """
    Creates a new optimization.
    If the optimization is created successfully, a 201 response with the base fields of the optimization is returned.
    If there is a validation error, a 422 response is returned.
    If there is an internal error, a 500 response is returned.
    """
    try:
        return controller.create_optimization(optimization_input_dto)
    except RuntimeError as e:
        return JSONResponse(status_code=500, content={'message': str(e)})


@router.get('/optimizations',
            summary='Get base fields of all currently registered optimizations, if available.',
            status_code=status.HTTP_200_OK,
            response_model=List[OptimizationOutputBaseDTO],
            responses={
                200: {'description': 'Successful Response',
                      'content': {
                          'application/json': {
                              'example': [{
                                  'optimization_id': 'UUID',
                                  'enums': 'ENUM',
                              }]
                          }
                      }}
            })
def get_optimizations() -> List[OptimizationOutputBaseDTO]:
    """
    Returns all base fields of available optimizations with response code 200.
    """
    return controller.get_optimizations()


@router.get('/optimizations/{optimization_id}',
            summary='Get the full description of a specific currently registered optimizations, if available.',
            status_code=status.HTTP_200_OK,
            response_model=OptimizationOutputDTO,
            responses={
                200: {'description': 'Successful Response',
                      'content': {
                          'application/json': {
                              'example': {
                                  'optimization_id': 'UUID',
                                  'status': 'ENUM',
                                  'problem': {},
                                  'framework': {},
                                  'statistics': {},
                              }
                          }
                      }},
                Response.OPTIMIZATION_NOT_FOUND.value[0]: {
                    'description': 'Optimization not found',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_NOT_FOUND.value[1]}'}
                        }
                    }
                }
            })
def get_optimization(optimization_id: UUID) -> JSONResponse | OptimizationOutputDTO:
    """
    Returns the full description of an optimization by ID with response code 200.
    If no optimization is found, a 404 response is returned.
    If there is a validation error, a 422 response is returned.
    """
    optimization = controller.get_optimization(optimization_id)

    if not isinstance(optimization, OptimizationOutputDTO):
        return JSONResponse(status_code=optimization.value[0],
                            content={'message': optimization.format_message(optimization_id=optimization_id)})

    return optimization


@router.get('/optimizations/{optimization_id}/statistics',
            summary='Get the statistics of a specific currently registered optimization, if available.',
            status_code=status.HTTP_200_OK,
            response_model=OptimizationOutputStatisticsDTO,
            responses={
                200: {'description': 'Successful Response',
                      'content': {
                          'application/json': {
                              'example': {
                                  'optimization_id': 'UUID',
                                  'status:': 'ENUM',
                                  'statistics': {
                                      'time_optimization_created': 'DATETIME',
                                      'time_run_started': 'DATETIME',
                                      'time_run_finished': 'DATETIME',
                                      'populations': []
                                  }
                              }
                          }
                      }},
                Response.OPTIMIZATION_NOT_FOUND.value[0]: {
                    'description': 'Optimization not found',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_NOT_FOUND.value[1]}'}
                        }
                    }
                }
            })
def get_optimization_statistics(optimization_id: UUID) -> JSONResponse | OptimizationOutputStatisticsDTO:
    """
    Returns the statistics of an optimization by ID with response code 200.
    If no optimization is found, a 404 response is returned.
    If there is a validation error, a 422 response is returned.
    """
    optimization_statistics = controller.get_optimization_statistics(optimization_id)

    if not isinstance(optimization_statistics, OptimizationOutputStatisticsDTO):
        return JSONResponse(status_code=optimization_statistics.value[0],
                            content={'message': optimization_statistics.format_message(optimization_id=optimization_id)})

    return optimization_statistics


@router.get('/optimizations/{optimization_id}/result',
            summary='Get the result of a specific currently registered optimization, if available.',
            status_code=status.HTTP_200_OK,
            response_model=OptimizationOutputResultDTO,
            responses={
                200: {'description': 'Successful Response',
                      'content': {
                          'application/json': {
                              'example': {
                                  'optimization_id': 'UUID',
                                  'status': 'ENUM',
                                  'problem': {
                                      'flights': [],
                                      'target_times': [],
                                      'result_flight_lists': []
                                  }
                              }
                          }
                      }},
                Response.OPTIMIZATION_NOT_FOUND.value[0]: {
                    'description': 'Optimization not found',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_NOT_FOUND.value[1]}'}
                        }
                    }
                }
            })
def get_optimization_result(optimization_id: UUID) -> JSONResponse | OptimizationOutputResultDTO:
    """
    Returns the result of an optimization by ID with response code 200.
    If no optimization is found, a 404 response is returned.
    If there is a validation error, a 422 response is returned.
    """
    optimization_result = controller.get_optimization_result(optimization_id)

    if not isinstance(optimization_result, OptimizationOutputResultDTO):
        return JSONResponse(status_code=optimization_result.value[0],
                            content={'message': optimization_result.format_message(optimization_id=optimization_id)})

    return optimization_result


@router.put('/optimizations/{optimization_id}/start',
            summary='If available, start an asynchronous run for a specific optimization that was previously created and initialized.',
            response_model=OptimizationOutputBaseDTO,
            responses={
                200: {'description': 'Asynchronous optimization run started',
                      'content': {
                          'application/json': {
                              'example': {
                                  'optimization_id': 'UUID',
                                  'status': 'RUNNING',
                              }
                          }
                      }},
                Response.OPTIMIZATION_NOT_FOUND.value[0]: {
                    'description': 'Optimization not found',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_NOT_FOUND.value[1]}'}
                        }
                    }
                },
                Response.OPTIMIZATION_ALREADY_STARTED.value[0]: {
                    'description': 'Optimization already started',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_ALREADY_STARTED.value[1]}'}
                        }
                    }
                }
            })
async def start_optimization(optimization_id: UUID) -> JSONResponse | OptimizationOutputBaseDTO:
    """
    Starts an asynchronous optimization run.
    If the optimization run is started successfully, a 200 response with the optimization base fields is returned.
    If the optimization is not found, a 404 response is returned.
    If the optimization has already been started, a 409 response is returned.
    """
    optimization = controller.start_optimization(optimization_id, async_run=True)

    if not isinstance(optimization, OptimizationOutputBaseDTO):
        return JSONResponse(status_code=optimization.value[0],
                            content={'message': optimization.format_message(optimization_id=optimization_id)})

    return optimization


@router.put('/optimizations/{optimization_id}/start/wait',
            summary='If available, start a synchronous run for a specific optimization that was previously created and initialized and wait for it to finish.',
            status_code=status.HTTP_200_OK,
            response_model=OptimizationOutputBaseDTO,
            responses={
                200: {'description': 'Synchronous optimization run started and finished',
                      'content': {
                          'application/json': {
                              'example': {
                                  'optimization_id': 'UUID',
                                  'status': 'FINISHED',
                              }
                          }
                      }},
                Response.OPTIMIZATION_NOT_FOUND.value[0]: {
                    'description': 'Optimization not found',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_NOT_FOUND.value[1]}'}
                        }
                    }
                },
                Response.OPTIMIZATION_ALREADY_STARTED.value[0]: {
                    'description': 'Optimization already started',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_ALREADY_STARTED.value[1]}'}
                        }
                    }
                }
            })
def start_optimization_wait(optimization_id: UUID) -> JSONResponse | OptimizationOutputBaseDTO:
    """
    Starts a synchronous optimization run.
    If the optimization run is finished, a 200 response with the optimization base is returned.
    If the optimization is not found, a 404 response is returned.
    If the optimization has already been started, a 409 response is returned.
    """
    optimization = controller.start_optimization(optimization_id, async_run=False)

    if not isinstance(optimization, OptimizationOutputBaseDTO):
        return JSONResponse(status_code=optimization.value[0],
                            content={'message': optimization.format_message(optimization_id=optimization_id)})

    return optimization


@router.put('/optimizations/{optimization_id}/abort',
            summary='If available, abort a previously started asynchronous optimization run; If available, an intermediate result can be obtained.',
            status_code=status.HTTP_200_OK,
            response_model=OptimizationOutputBaseDTO,
            responses={
                200: {'description': 'Synchronous optimization run started and finished',
                      'content': {
                          'application/json': {
                              'example': {
                                  'optimization_id': 'UUID',
                                  'status': 'ABORTED',
                              }
                          }
                      }},
                Response.OPTIMIZATION_NOT_FOUND.value[0]: {
                    'description': 'Optimization not found',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_NOT_FOUND.value[1]}'}
                        }
                    }
                },
                Response.OPTIMIZATION_NOT_RUNNING.value[0]: {
                    'description': 'Optimization not running',
                    'content': {
                        'application/json': {
                            'example': {'message': f'{Response.OPTIMIZATION_NOT_RUNNING.value[1]}'}
                        }
                    }
                }
            })
def abort_optimization(optimization_id: UUID) -> JSONResponse | OptimizationOutputBaseDTO:
    """
    Aborts a running asynchronous optimization run.
    If the optimization run is aborted successfully, a 200 response with the optimization base is returned.
    If the optimization is not found, a 404 response is returned.
    If the optimization is not running, a 409 response is returned.
    """
    optimization = controller.abort_optimization(optimization_id)

    if not isinstance(optimization, OptimizationOutputBaseDTO):
        return JSONResponse(status_code=optimization.value[0],
                            content={'message': optimization.format_message(optimization_id=optimization_id)})

    return optimization


@router.delete('/optimizations/{optimization_id}',
               summary='If available, delete an optimization and its results; If available, abort a running optimization.',
               status_code=status.HTTP_200_OK,
               responses={
                   Response.OPTIMIZATION_DELETED.value[0]: {
                       'description': 'Optimization deleted successfully',
                       'content': {
                           'application/json': {
                               'example': {'message': f'{Response.OPTIMIZATION_DELETED.value[1]}'}
                           }
                       }
                   },
                   Response.OPTIMIZATION_NOT_FOUND.value[0]: {
                       'description': 'Optimization not found',
                       'content': {
                           'application/json': {
                               'example': {'message': f'{Response.OPTIMIZATION_NOT_FOUND.value[1]}'}
                           }
                       }
                   },
                   Response.OPTIMIZATION_CURRENTLY_RUNNING.value[0]: {
                       'description': 'Optimization currently running',
                       'content': {
                           'application/json': {
                               'example': {'message': f'{Response.OPTIMIZATION_CURRENTLY_RUNNING.value[1]}'}
                           }
                       }
                   },
               })
def delete_optimization(optimization_id: UUID) -> JSONResponse:
    """
    Deletes an optimization.
    If the optimization is deleted successfully, a 200 response is returned.
    If the optimization is not found, a 404 response is returned.
    If the optimization is currently running, a 409 response is returned.
    """
    delete = controller.delete_optimization(optimization_id)

    return JSONResponse(status_code=delete.value[0],
                        content={'message': delete.format_message(optimization_id=optimization_id)})
