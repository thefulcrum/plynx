import { combineReducers } from 'redux'


const setApiDialogVisibility = (state = false, action) => {
  switch (action.type) {
    case 'SET_API_DIALOG_VISIBILITY_FILTER':
      return action.value
    default:
      return state
  }
}


export default combineReducers({
  setApiDialogVisibility,
})
