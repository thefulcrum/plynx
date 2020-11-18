import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import SortableTree from "react-sortable-tree";
import { DropTarget } from 'react-dnd';
import ItemTypes from '../../DragAndDropsItemTypes';


// a little function to help us with reordering the result
const reorder = (list, startIndex, endIndex) => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);

  return result;
};

// TODO unite with react_node_graph
const getScrollOffset = () => {
  const el = document.getElementsByClassName('GraphRoot')[0];
  return {
    x: el.scrollLeft,
    y: el.scrollTop,
  };
};


const boxTarget = {
  drop(props, monitor, component) {     // eslint-disable-line no-unused-vars
    const groupProps = props;
    const blockObj = monitor.getItem();
    const mousePos = monitor.getClientOffset();
    console.log('c', blockObj);

    if (groupProps.onDrop) {
      // Hack: use GraphRoot scroll position
      const offset = getScrollOffset();
      groupProps.onDrop({
        nodeContent: blockObj.nodeContent,
        mousePos: {
          x: mousePos.x + offset.x,
          y: mousePos.y + offset.y,
        },
      });
    }
    return { name: 'ReactBlockGraph' };
  },
};

function findError(treeDataChildren) {
  console.log('findError', treeDataChildren);
  if (!treeDataChildren) {
      return false;
  }
  for (const treeData of treeDataChildren) {
      if (treeData.children && treeData.children.length > 0) {
        if (treeData.canExpand !== undefined && !treeData.canExpand) {
            return true;
        }
        if (findError(treeData.children)) {
            return true;
        }
      }
  }
  return false;
}

class DirectoryColumn extends Component {
  constructor(props) {
    super(props);
    this.state = {
      treeData: props.treeData,
      readOnly: false
    };
    console.log('props', this.props);

    this.onDragEnd = this.onDragEnd.bind(this);
  }

  onDragEnd(result) {
    // dropped outside the list
    if (!result.destination) {
      return;
    }

    const items = reorder(
      this.state.items,
      result.source.index,
      result.destination.index
    );

    this.setState({
      items,
    });
    // this.props.onChanged(items);
  }

  handleChangeTree(treeData) {
    console.log(treeData);
    //this.setState({ treeData });
    if (!findError(treeData)) {
      this.setState({ treeData });
    }
  }

  handleChanged(index, name, value) {
    const items = this.state.items;
    items[index][name] = value;
    this.setState({items: items});
    this.props.onChanged(items);
  }

  handleRemoveItem(index) {
    const items = this.state.items;
    items.splice(index, 1);
    this.setState({items: items});
    this.props.onChanged(items);
  }

  // Normally you would want to split things out into separate components.
  // But in this example everything is just done in one place for simplicity
  render() {
    const { connectDropTarget } = this.props;

    return connectDropTarget(
      <div className='group-main'>
          <SortableTree
            treeData={this.state.treeData}
            onChange={(treeData) => this.handleChangeTree(treeData)}
              //theme={FileExplorerTheme}
             className="group-directory"
          />
      </div>
    );
  }
}

export default DropTarget(ItemTypes.NODE_ITEM, boxTarget, (connect, monitor) => ({
  connectDropTarget: connect.dropTarget(),
  isOver: monitor.isOver(),
  canDrop: monitor.canDrop(),
}))(DirectoryColumn);
