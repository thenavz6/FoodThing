(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(['exports', 'react', 'prop-types', 'styled-components'], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports, require('react'), require('prop-types'), require('styled-components'));
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports, global.react, global.propTypes, global.styledComponents);
    global.dropdown = mod.exports;
  }
})(this, function (exports, _react, _propTypes, _styledComponents) {
  'use strict';

  Object.defineProperty(exports, "__esModule", {
    value: true
  });

  var _react2 = _interopRequireDefault(_react);

  var _propTypes2 = _interopRequireDefault(_propTypes);

  var _styledComponents2 = _interopRequireDefault(_styledComponents);

  function _interopRequireDefault(obj) {
    return obj && obj.__esModule ? obj : {
      default: obj
    };
  }

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }

  var _createClass = function () {
    function defineProperties(target, props) {
      for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value" in descriptor) descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
      }
    }

    return function (Constructor, protoProps, staticProps) {
      if (protoProps) defineProperties(Constructor.prototype, protoProps);
      if (staticProps) defineProperties(Constructor, staticProps);
      return Constructor;
    };
  }();

  function _possibleConstructorReturn(self, call) {
    if (!self) {
      throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }

    return call && (typeof call === "object" || typeof call === "function") ? call : self;
  }

  function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
      throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }

    subClass.prototype = Object.create(superClass && superClass.prototype, {
      constructor: {
        value: subClass,
        enumerable: false,
        writable: true,
        configurable: true
      }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
  }

  var _templateObject = _taggedTemplateLiteral(['\n  &.dropdown {\n    .dropdown__ul {\n      list-style-type: none;\n      margin: 0;\n      padding: 0;\n      border: 1px solid #f1f1f1;\n      border-top: 0;\n      border-radius: 3px;\n      border-top-right-radius: 0;\n      border-top-left-radius: 0;\n      max-height: calc(100vh - 100px);\n      overflow-y: auto;\n    }\n\n    .dropdown__ul__li {\n      padding: 10px;\n      font-size: 16px;\n      font-weight: 100;\n    }\n\n    .dropdown__ul__li:hover {\n      background-color: #f1f1f1;\n      cursor: pointer;\n    }\n  }\n'], ['\n  &.dropdown {\n    .dropdown__ul {\n      list-style-type: none;\n      margin: 0;\n      padding: 0;\n      border: 1px solid #f1f1f1;\n      border-top: 0;\n      border-radius: 3px;\n      border-top-right-radius: 0;\n      border-top-left-radius: 0;\n      max-height: calc(100vh - 100px);\n      overflow-y: auto;\n    }\n\n    .dropdown__ul__li {\n      padding: 10px;\n      font-size: 16px;\n      font-weight: 100;\n    }\n\n    .dropdown__ul__li:hover {\n      background-color: #f1f1f1;\n      cursor: pointer;\n    }\n  }\n']);

  function _taggedTemplateLiteral(strings, raw) {
    return Object.freeze(Object.defineProperties(strings, {
      raw: {
        value: Object.freeze(raw)
      }
    }));
  }

  var DropdownWrapper = _styledComponents2.default.div(_templateObject);

  var Dropdown = function (_Component) {
    _inherits(Dropdown, _Component);

    function Dropdown() {
      _classCallCheck(this, Dropdown);

      return _possibleConstructorReturn(this, (Dropdown.__proto__ || Object.getPrototypeOf(Dropdown)).apply(this, arguments));
    }

    _createClass(Dropdown, [{
      key: 'listNode',
      value: function listNode() {
        var _this2 = this;

        return _react2.default.createElement(
          'ul',
          { className: 'dropdown__ul' },
          this.props.data.map(function (list, index) {
            return _react2.default.createElement(
              'li',
              {
                key: index,
                className: 'dropdown__ul__li',
                onClick: _this2.props.onClick.bind(list['' + _this2.props.searchKey])
              },
              list['' + _this2.props.searchKey]
            );
          })
        );
      }
    }, {
      key: 'render',
      value: function render() {
        if (!this.props.show) {
          return false;
        }

        return _react2.default.createElement(
          DropdownWrapper,
          { className: 'dropdown' },
          this.listNode()
        );
      }
    }]);

    return Dropdown;
  }(_react.Component);

  Dropdown.propTypes = {
    data: _propTypes2.default.array,
    onClick: _propTypes2.default.func,
    show: _propTypes2.default.bool,
    searchKey: _propTypes2.default.string
  };
  Dropdown.defaultProps = {
    data: [],
    show: false
  };
  exports.default = Dropdown;
});